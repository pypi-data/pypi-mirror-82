""" Migrate country names
"""
import logging
import json
import transaction
from zope.component import queryMultiAdapter
from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from eea.geotags.rdf.country_groups import COUNTRY_GROUPS
try:
    from Products.EEAPloneAdmin.browser.migration_helper_data import (
        countryDicts,
    )
except ImportError:
    def countryDicts():
        """ EEAPloneAdmin not installed """
        return {}

logger = logging.getLogger(__name__)


def create_obj_uri(obj):
    """ """
    obj_url = obj.absolute_url(1)
    portalUrl = 'https://www.eea.europa.eu'
    if obj_url.find('www/SITE/') != -1:
        pub_url = portalUrl + obj_url[8:]
    else:
        pub_url = portalUrl + obj_url[3:]
    return pub_url


def set_location_field(obj, new_geotags, ping_cr_view):
    """ """
    loc_field = obj.getField('location')
    loc_field.set(obj, json.dumps(new_geotags))
    try:
        obj.reindexObject(idxs=['geotags', 'location'])
    except TypeError, err:
        logger.info("Error reindex object: %s" % obj.absolute_url())
        logger.error(err)
    ping_cr_view(create_obj_uri(obj))


def check_countries_from_grp(grp, features, country_groups_data):
    """ """
    missing_countries = {}
    for country in country_groups_data[grp]:
        for feature in features:
            title = feature['properties']['title']
            if country == title:
                try:
                    del missing_countries[country]
                except KeyError:
                    pass
                break
            missing_countries[country] = True
    return missing_countries


def migrate_country_names(context, content_type=None, email=None):
    """ migrate wrong country names and remove country groups
    """
    try:
        if not content_type:
            return 'Nothing to be done!'
        logger.info("Start fixing the country names!")
        request = getattr(context, 'REQUEST', None)
        ping_cr_view = queryMultiAdapter((context, request), name="ping_cr")
        pcat = getToolByName(context, "portal_catalog")
        query = {
            'portal_type': content_type,
            'Language': 'all',
        }
        brains = pcat(query)

        # create country names vocab
        country_name = {
            'Macedonia (ARYM)': 'North Macedonia',
            'Macedonia (FYR)': 'North Macedonia',
            'Macedonia (FYROM)': 'North Macedonia',
            'Macedonia': 'North Macedonia',
            'Former Yugoslav Republic of Macedonia, the': 'North Macedonia',
            'North Former Yugoslav Republic of Macedonia, the': 'North Macedonia',
            'Czech Republic': 'Czechia'
            # 'Kosova (Kosovo)': 'Kosovo (UNSCR 1244/99)',
            # 'Kosovo': 'Kosovo (UNSCR 1244/99)'
        }

        # create the country groups
        country_groups = COUNTRY_GROUPS
        country_groups_vocab = ['EEA32', 'EEA33', 'EFTA4', 'EU15',
            'EU25', 'EU27', 'EU28', 'Pan-Europe']
        country_groups_data = {}
        for gr in country_groups.keys():
            if gr[0] == 'PANE':
                country_groups_data['Pan-Europe'] = country_groups[gr]
                continue
            if gr[0] in country_groups_vocab:
                country_groups_data[gr[0]] = country_groups[gr]
        country_groups_data[u'EU32'] = [
            u'Cyprus',
            u'Portugal',
            u'Spain',
            u'Malta',
            u'Denmark',
            u'United Kingdom',
            u'Sweden',
            u'Netherlands',
            u'Austria',
            u'Belgium',
            u'Germany',
            u'Luxembourg',
            u'Ireland',
            u'France',
            u'Slovakia',
            u'Czechia',
            u'Italy',
            u'Slovenia',
            u'Greece',
            u'Croatia',
            u'Estonia',
            u'Latvia',
            u'Lithuania',
            u'Finland',
            u'Hungary',
            u'Bulgaria',
            u'Poland',
            u'Romania',
            u'Switzerland',
            u'Iceland',
            u'Liechtenstein',
            u'Norway',
            u'Turkey',
        ]

        correct_macedonia = 'North Macedonia'
        total_brains_number = len(brains)
        logger.info("Start checking %s objects." % total_brains_number)
        obj_with_groups = {}
        obj_with_bad_country_name = {}
        obj_with_bad_russia = {}
        count_countries_detected = 0
        count_groups_detected = 0
        update_detected = False
        count_progress = 0

        for brain in brains:
            count_progress += 1
            update_detected = False

            try:
                obj = brain.getObject()
            except Exception as err:
                logger.exception("%s - %s", brain.getURL(), err)
                continue
            obj_uri = obj.absolute_url()
            anno = getattr(obj, '__annotations__', {})
            geotags = anno.get('eea.geotags.tags')
            if not geotags:
                continue
            features = geotags.get('features')

            # detect country name containing "Russian Federation"
            for feature in features:
                title = feature['properties']['title']
                description = feature['properties']['description']
                if ('Russia' in title) or ('Russia' in description):
                    update_detected = True
                    obj_with_bad_russia[obj_uri] = True
                if 'Russian Federation' in title:
                    title = title.replace('Russian Federation', 'Russia')
                    feature['properties']['title'] = title
                    update_detected = True
                    obj_with_bad_russia[obj_uri] = True
                if 'Russian Federation' in description:
                    description = description.replace('Russian Federation', 'Russia')
                    feature['properties']['description'] = description
                    update_detected = True
                    obj_with_bad_russia[obj_uri] = True

            # detect country name to be replaced
            for country in country_name.keys():
                for feature in features:
                    title = feature['properties']['title']
                    description = feature['properties']['description']
                    if country in title:
                        if country == "Macedonia" and "Greece" in description:
                            continue
                        if "Macedonia" in country:
                            if title != correct_macedonia:
                                feature['properties']['title'] = correct_macedonia
                                update_detected = True
                                count_countries_detected += 1
                                obj_with_bad_country_name[obj_uri] = True
                            continue
                        if country == "Kosovo" and 'Kosovo (UNSCR 1244/99)' in title:
                            continue
                        if country == "Kosovo" and 'Kosova (Kosovo)' in title:
                            continue
                        title = title.replace(country, country_name[country])
                        feature['properties']['title'] = title
                        update_detected = True
                        count_countries_detected += 1
                        obj_with_bad_country_name[obj_uri] = True

                for feature in features:
                    description = feature['properties']['description']
                    if country in description:
                        if country == "Macedonia" and "Greece" in description:
                            continue
                        if "Macedonia" in country:
                            if description != correct_macedonia:
                                feature['properties']['description'] = correct_macedonia
                                update_detected = True
                                count_countries_detected += 1
                                obj_with_bad_country_name[obj_uri] = True
                            continue
                        if country == "Kosovo" and 'Kosovo (UNSCR 1244/99)' in description:
                            continue
                        if country == "Kosovo" and 'Kosova (Kosovo)' in description:
                            continue
                        description = description.replace(country, country_name[country])
                        feature['properties']['description'] = description
                        update_detected = True
                        count_countries_detected += 1
                        obj_with_bad_country_name[obj_uri] = True

            # detect country group assigned
            features_to_remove = []
            features_to_be_added = []
            for grp in country_groups_data.keys():
                for feature in features:
                    _u = lambda t: t.decode('UTF-8', 'replace') if isinstance(t, str) else t 
                    title = _u(feature['properties']['title'])

                    if grp in title:
                        update_detected = True
                        count_groups_detected += 1
                        obj_with_groups[obj_uri] = True
                        # check if all countries from the group are in features
                        missing_countries = check_countries_from_grp(grp, features, country_groups_data)
                        # add missing countries data
                        for country in missing_countries:
                            features_to_be_added.append(countryDicts()[country])
                        # mark country group to be removed
                        features_to_remove.append(feature)

            for feature in features_to_remove:
                features.remove(feature)
            for feature in features_to_be_added:
                features.append(feature)

            # update object, reindex catalog and ping SDS
            if update_detected:
                geo_data = {}
                geo_data['features'] = features
                geo_data['type'] = geotags['type']
                set_location_field(obj, geo_data, ping_cr_view)
                logger.info("Updated: %s" % obj_uri)

            # display progress
            if not (count_progress % 10):
                transaction.commit()
                logger.info("#################### Progress: %s/%s objects checked." % (count_progress, total_brains_number))

        logger.info("#################### Found 'Russian Federation' in %s objects:" % len(obj_with_bad_russia.keys()))
        for k in obj_with_bad_russia.keys():
            logger.info(k)
        logger.info("#################### Found %s bad country names in %s objects:" % (count_countries_detected, len(obj_with_bad_country_name.keys())))
        for k in obj_with_bad_country_name.keys():
            logger.info(k)
        logger.info("#################### Found %s groups in %s objects:" % (count_groups_detected, len(obj_with_groups.keys())))
        for k in obj_with_groups.keys():
            logger.info(k)
        if email:
            mailhost = getToolByName(context, 'MailHost')
            text = """Finished fixing country names for '%s'. """ % content_type
            email_from = "no-reply@eea.europa.eu"
            subject = "Macedonia data migration for: %s" % content_type

            return_msg = "Sending email for %s ." % content_type

            try:
                logger.info('Sending e-mail to %s', email)
                mailhost.send(messageText=text, mfrom=email_from, mto=email,
                    subject=subject)
            except Exception, e:
                logger.error("Got exception %s for %s", e, email)
                return_msg += "Error raised while attempting to send e-mail. "
            else:
                return_msg += "E-mail sent. "
            logger.info(return_msg)
        logger.info("Done fixing the country names!")
    except Exception, err:
        if email:
            mailhost = getToolByName(context, 'MailHost')
            text = """ Migration script failed for '%s' with error: %s """ % (content_type, err)
            email_from = "no-reply@eea.europa.eu"
            subject = "Macedonia data migration FAILURE for: %s" % content_type

            return_msg = "Sending email for %s ." % content_type

            try:
                logger.info('Sending e-mail to %s', email)
                mailhost.send(messageText=text, mfrom=email_from, mto=email,
                    subject=subject)
            except Exception, e:
                logger.error("Got exception %s for %s", e, email)
                return_msg += "Error raised while attempting to send e-mail. "
            else:
                return_msg += "E-mail sent."
            logger.info(return_msg)
        logger.error("Got exception %s for %s", err, content_type)
    

class MigrateCountryNames(BrowserView):
    """ Migrate country names and remove groups
    """
    def __call__(self, **kwargs):
        content_type = self.request.get('ctype', None)
        email = self.request.get('email', None)
        if content_type:
            migrate_country_names(self.context, content_type, email)
            return "Done!"
        else:
            return 'Please add "ctype" parameter!'
            