from django.core.management.base import BaseCommand
from apps.portfolio.models import OOSBlurb


BLURBS = [
    # ── Negative experiences ────────────────────────────────────────────────
    dict(platform='tweet', sentiment='bad', light_mode=False,
         live_dur=4.5, live_delay=0.0, sort_order=10,
         author_name='Sarah Chen', author_handle='@sarah_chen', avatar_color='#e07060',
         body_text='Tried to find their hours online. Website looks like it\'s from 2008. Just went to a competitor.'),

    dict(platform='email', sentiment='bad', light_mode=True,
         live_dur=6.2, live_delay=1.4, sort_order=20,
         from_email='customer@gmail.com', subject='Couldn\'t find your contact form?',
         body_text='Hi, I tried reaching out through your website but the form doesn\'t work. I\'ve been trying for three days…'),

    dict(platform='tweet', sentiment='bad', light_mode=False,
         live_dur=3.8, live_delay=2.1, sort_order=30,
         author_name='Mike R.', author_handle='@mike_reviews', avatar_color='#7b68ee',
         body_text='No mobile site? Contact form gives a 404. In 2025. Unbelievable.'),

    dict(platform='sms', sentiment='bad', light_mode=False,
         live_dur=5.5, live_delay=0.7, sort_order=40,
         sms_1_dir='in',  sms_1_text='did you find their address?',
         sms_2_dir='out', sms_2_text='nope their site is broken lol',
         sms_3_dir='in',  sms_3_text='just go to the other place'),

    dict(platform='review', sentiment='bad', light_mode=False,
         live_dur=7.0, live_delay=1.8, sort_order=50,
         star_count=3, reviewer_label='Google Review, 2024',
         body_text='"Couldn\'t find hours or pricing. Site looked abandoned. Not sure if they\'re even open."'),

    dict(platform='yelp', sentiment='bad', light_mode=True,
         live_dur=4.2, live_delay=3.0, sort_order=60,
         star_count=2,
         body_text='"Great place but wrong hours on the website. Drove 20 minutes and they were closed."'),

    # ── Positive experiences ────────────────────────────────────────────────
    dict(platform='tweet', sentiment='good', light_mode=True,
         live_dur=5.8, live_delay=2.5, sort_order=70,
         author_name='James Liu', author_handle='@jliu_design', avatar_color='#2ecc71',
         body_text='They just relaunched with a new site. Stunning. Made a booking immediately ✨'),

    dict(platform='email', sentiment='good', light_mode=False,
         live_dur=3.5, live_delay=0.3, sort_order=80,
         from_email='newclient@outlook.com', subject='Found you through your website!',
         body_text='Your website is gorgeous and so easy to navigate. Signed up immediately — exactly what I was looking for.'),

    dict(platform='sms', sentiment='good', light_mode=True,
         live_dur=6.8, live_delay=1.1, sort_order=90,
         sms_1_dir='in',  sms_1_text='have you seen their new site??',
         sms_2_dir='out', sms_2_text='omg booked already'),

    dict(platform='instagram', sentiment='bad', light_mode=False,
         live_dur=4.0, live_delay=2.8, sort_order=100,
         ig_username='@their_business', ig_followers='123 followers', ig_likes='12 likes',
         body_text='Check out our new products! Visit our website to learn more (link in bio)'),

    dict(platform='instagram', sentiment='good', light_mode=True,
         live_dur=5.2, live_delay=0.5, sort_order=110,
         ig_username='@their_business', ig_followers='4,821 followers', ig_likes='847 likes',
         body_text='New website just launched — link in bio to book your first session!'),

    dict(platform='review', sentiment='good', light_mode=False,
         live_dur=7.5, live_delay=1.7, sort_order=120,
         star_count=5, reviewer_label='Google Review, 2025',
         body_text='"Beautifully designed website. Booked my first lesson within 5 minutes of landing on the page."'),

    # ── Additional cards (×2 density) ───────────────────────────────────────
    dict(platform='tweet', sentiment='bad', light_mode=False,
         live_dur=5.1, live_delay=0.9, sort_order=130,
         author_name='Jordan T.', author_handle='@jordantalks', avatar_color='#9b59b6',
         body_text='their website took 14 seconds to load on mobile. i timed it. moved on.'),

    dict(platform='sms', sentiment='bad', light_mode=True,
         live_dur=4.8, live_delay=2.3, sort_order=140,
         sms_1_dir='in',  sms_1_text='did you book it',
         sms_2_dir='out', sms_2_text='their site is broken',
         sms_3_dir='in',  sms_3_text='use yelp instead'),

    dict(platform='email', sentiment='bad', light_mode=False,
         live_dur=6.5, live_delay=1.2, sort_order=150,
         from_email='hungry@gmail.com', subject='Can\'t access your menu?',
         body_text='Hi, your menu link says "page not found." We had to guess what you serve.'),

    dict(platform='review', sentiment='bad', light_mode=False,
         live_dur=5.8, live_delay=0.4, sort_order=160,
         star_count=2, reviewer_label='Google Review, 2024',
         body_text='"Wrong address listed on website. Drove across town for nothing."'),

    dict(platform='tweet', sentiment='bad', light_mode=False,
         live_dur=3.5, live_delay=1.6, sort_order=170,
         author_name='Priya K.', author_handle='@priyarants', avatar_color='#e74c3c',
         body_text='no hours. no phone number. no map. literally what is the website even for'),

    dict(platform='yelp', sentiment='bad', light_mode=False,
         live_dur=4.8, live_delay=2.9, sort_order=180,
         star_count=1,
         body_text='"Photos all broken. Menu link 404s. The food was fine though."'),

    dict(platform='tweet', sentiment='good', light_mode=True,
         live_dur=6.0, live_delay=0.6, sort_order=190,
         author_name='Alex Morgan', author_handle='@alexm_fits', avatar_color='#1abc9c',
         body_text='found them through their website — booking was so smooth. instant trust.'),

    dict(platform='sms', sentiment='good', light_mode=False,
         live_dur=5.4, live_delay=1.9, sort_order=200,
         sms_1_dir='in',  sms_1_text='omg found them online',
         sms_2_dir='out', sms_2_text='their site is SO good',
         sms_3_dir='in',  sms_3_text='booked already 🎉'),

    dict(platform='email', sentiment='good', light_mode=True,
         live_dur=4.6, live_delay=0.8, sort_order=210,
         from_email='tasha@gmail.com', subject='Just wanted to say...',
         body_text='Your new website is stunning. Found everything I needed in under a minute.'),

    dict(platform='review', sentiment='good', light_mode=True,
         live_dur=7.2, live_delay=2.2, sort_order=220,
         star_count=5, reviewer_label='Google Review, 2025',
         body_text='"Found them on Google, website sold me immediately. Booked before even calling."'),

    dict(platform='instagram', sentiment='good', light_mode=False,
         live_dur=5.6, live_delay=3.2, sort_order=230,
         ig_username='@their_business', ig_followers='12,400 followers', ig_likes='2,341 likes',
         body_text='Thank you for all the love since the rebrand 🙏'),

    dict(platform='tweet', sentiment='good', light_mode=False,
         live_dur=4.3, live_delay=1.5, sort_order=240,
         author_name='Dana P.', author_handle='@danaphotos', avatar_color='#f39c12',
         body_text='honestly the best small business website I\'ve seen. bookmarked and booked. ✨'),
]


class Command(BaseCommand):
    help = 'Seed the 24 default OOS blurbs for the web_dev scatter section'

    def add_arguments(self, parser):
        parser.add_argument(
            '--reset', action='store_true',
            help='Delete all existing OOSBlurb records before seeding'
        )

    def handle(self, *args, **options):
        if options['reset']:
            deleted, _ = OOSBlurb.objects.all().delete()
            self.stdout.write(self.style.WARNING(f'Deleted {deleted} existing blurbs.'))

        if OOSBlurb.objects.exists() and not options['reset']:
            self.stdout.write(self.style.NOTICE('OOS blurbs already exist. Use --reset to replace them.'))
            return

        created = 0
        for data in BLURBS:
            OOSBlurb.objects.create(**data)
            created += 1

        self.stdout.write(self.style.SUCCESS(f'Created {created} OOS blurbs.'))
