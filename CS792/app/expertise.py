# This file contains dictionaries of expert knowledge, 
# including advertising websites, credible websites, and special domain names.


ads = set([])

# Credible websites listed by Dr. Hafeez.

sources_armughan = set(['rochestergeneral.org', 'stanfordhealthcare.org/',
                       'corephysicians.org',
                       'general.surgery.ucsf.edu/conditions--procedures/gallstones-(cholelithiasis).aspx',
                       'hb.surgery.ucsf.edu/', 'en.wikipedia.org/wiki/Biliary_tract',
                       'radiopaedia.org/articles/hepatobiliary-contrast-agents-and-li-rads'])


# Credible webistes listed by Hiffington Post at
# http://www.huffingtonpost.com/jim-t-miller/online-medical-information_b_3667454.html.

sources_huffington = set(['medlineplus.gov', 'mayoclinic.com', 'nihseniorhealth.gov'])

# Credible websites listed by Health Service at University of Michigan at https://www.uhs.umich.edu/websites.

sources_umich = set(['cdc.gov/', 'familydoctor.org/', '4collegewomen.org/',
                    'goaskalice.columbia.edu/', 'healthfinder.gov/',
                    'intelihealth.com/', 'mlanet.org/resources',
                    'mercksource.com/', 'womenshealth.gov/', 'noah-health.org/',
                    'webmd.com'])

# Credible websites listed by Johns Hopkins University at
# http://www.hopkinsmedicine.org/johns_hopkins_bayview/patient_visitor_amenities/
# community_health_library/finding_reliable_health_information_online.html.

sources_jhu = set(['pillbox.nlm.nih.gov', 'consumermedsafety.org', 'hopkinsmedicine.org', 'hospitalcompare.hhs.gov',
                  'nami.org', 'kidshealth.org', 'knowyourteeth.com'])

# Source integration.
ls = [sources_armughan, sources_huffington, sources_jhu, sources_umich]
source = set().union(*ls)

# Other potential sources- Medical Library Association: http://caphis.mlanet.org/consumer/top100all.pdf

# According to NIH, these domain names should be considered more credible.
# https://www.nia.nih.gov/health/publication/online-health-information

domains = set(['.gov', '.edu', '.org'])
