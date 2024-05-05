
def get_user_avatar(user):
    # Assuming you have a one-to-one relationship between User and Profile
    # and the profile model has the image field
    try:
        return user.image.url  # Assuming 'Profile' is the related model and 'image' is the field
    except:
        return '/static/image/jazzmin-admin/7309681.jpg'


JAZZMIN_SETTINGS = {
    # title of the window (Will default to current_admin_site.site_title if absent or None)
    "site_title": "NeymanTech Enterprise", # tabda yazilan yazi

    # Title on the login screen (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    "site_header": "NeymanTech", # sekil olmasa cixacaq yazi

    # Title on the brand (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    "site_brand": "NeymanTech Admin",

    # Logo to use for your site, must be present in static files, used for brand on top left
    "site_logo": "image/jazzmin-admin/neymanlogo.png", # admin paneldeki logo yuxari solda

    # Logo to use for your site, must be present in static files, used for login form logo (defaults to site_logo)
    "login_logo": 'image/jazzmin-admin/new1.png', # login sehifesindeki logo

    # Logo to use for login form in dark themes (defaults to login_logo)
    "login_logo_dark": None,

    # CSS classes that are applied to the logo above
    "site_logo_classes": "img-circle", # sekilin dairevi olmasi

    # Relative path to a favicon for your site, will default to site_logo if absent (ideally 32x32 px)
    "site_icon": None,

    # Welcome text on the login screen
    "welcome_sign": "Welcome to the NeymanTech Admin Site",

    # Copyright on the footer
    "copyright": "NeymanTech EnterPrise",

    # List of model admins to search from the search bar, search bar omitted if excluded
    # If you want to use a single search field you dont need to use a list, you can use a simple string 
    "search_model": ["Account.User", "Blog.Blog"],

    # Field name on user model that contains avatar ImageField/URLField/Charfield or a callable that receives the user
    "user_avatar": get_user_avatar,

    ############
    # Top Menu #
    ############

    # Links to put along the top menu
    "topmenu_links": [

        # Url that gets reversed (Permissions can be added)
        {"name": "Home",  "url": "admin:index", "permissions": ["auth.view_user"]},

        # external url that opens in a new window (Permissions can be added)
        {"name": "Website", "url": "https://neymantech.com/", "new_window": True},

        # # model admin to link to (Permissions checked against model)
        # {"model": "Blog.Blog"},

        # # App with dropdown menu to all its models pages (Permissions checked against models)
        {"app": "Blog"},
    ],

    #############
    # User Menu #
    #############

    # Additional links to include in the user menu on the top right ("app" url type is not allowed)
    # "usermenu_links": [
    #     {"name": "Support", "url": "https://github.com/farridav/django-jazzmin/issues", "new_window": True},
    #     {"model": "auth.user"}
    # ],

    #############
    # Side Menu #
    #############

    # Whether to display the side menu
    # "show_sidebar": True,

    # Whether to aut expand the menu
    "navigation_expanded": False,

    # Hide these apps when generating side menu e.g (auth)
    # "hide_apps": [],
    "hide_apps": ['auth'],

    # Hide these models when generating side menu (e.g auth.user)
    "hide_models": [],
    # "hide_models": ['Blog.Blog'],

    # List of apps (and/or models) to base side menu ordering off of (does not need to contain all apps/models)
    "order_with_respect_to": ["Account", "About"],

    # Custom links to append to app groups, keyed on app name
    # "custom_links": {
    #     "About": [{
    #         "name": "Make Messages",
    #         "url": "make_messages",
    #         "icon": "fas fa-comments",
    #         "permissions": ["books.view_book"]
    #     }]
    # },

    # Custom icons for side menu apps/models See https://fontawesome.com/icons?d=gallery&m=free&v=5.0.0,5.0.1,5.0.10,5.0.11,5.0.12,5.0.13,5.0.2,5.0.3,5.0.4,5.0.5,5.0.6,5.0.7,5.0.8,5.0.9,5.1.0,5.1.1,5.2.0,5.3.0,5.3.1,5.4.0,5.4.1,5.4.2,5.13.0,5.12.0,5.11.2,5.11.1,5.10.0,5.9.0,5.8.2,5.8.1,5.7.2,5.7.1,5.7.0,5.6.3,5.5.0,5.4.2
    # for the full list of 5.13.0 free icon classes
    "icons": {
        "Account": "fas fa-users-cog",
        "Account.User": "fas fa-users",
        # About
        "About": "fas fa-info-circle",
        "About.ContactInfo": "fas fa-address-book",
        "About.DifferentUs": "fas fa-puzzle-piece",
        "About.EmailAddress": "fas fa-envelope",
        "About.PhoneNumber": "fas fa-phone",
        # Blog
        "Blog": "fas fa-book",
        "Blog.Blog": "fas fa-newspaper",
        "Blog.BlogCategory": "fas fa-tag",
        # Core
        # "Core": "fas fa-hub",
        # "Core": "fas fa-cogs",
        "Core": "fas fa-atom",
        "Core.FAQ": "fas fa-question-circle",
        "Core.Partner": "fas fa-handshake",
        "Core.Subscribe": "fas fa-envelope",
        # Project
        "Project": "fas fa-project-diagram",
        "Project.Project": "fas fa-tasks",
        "Project.ProjectAllImage": "fas fa-images",
        # Request
        "Request": "fas fa-concierge-bell",
        "Request.WebsiteRequest": "fas fa-bell",
        # Review
        "Review": "fas fa-star",
        "Review.CostumerReview": "fas fa-comment",
        # Service
        "Service": "fas fa-cogs",
        "Service.Service": "fas fa-tools",
        "Service.ServiceCard": "fas fa-ellipsis-v",
    },
    # Icons that are used when one is not manually specified
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",

    #################
    # Related Modal #
    #################
    # Use modals instead of popups
    # "related_modal_active": False,

    #############
    # UI Tweaks #
    #############
    # Relative paths to custom CSS/JS scripts (must be present in static files)
    "custom_css": None,
    "custom_js": None,
    # Whether to link font from fonts.googleapis.com (use custom_css to supply font otherwise)
    "use_google_fonts_cdn": True,
    # Whether to show the UI customizer on the sidebar
    "show_ui_builder": True,

    ###############
    # Change view #
    ###############
    # Render out the change view as a single form, or in tabs, current options are
    # - single
    # - horizontal_tabs (default)
    # - vertical_tabs
    # - collapsible
    # - carousel
    "changeform_format": "horizontal_tabs",
    # override change forms on a per modeladmin basis
    # "changeform_format_overrides": {"Account.user": "collapsible", "auth.group": "vertical_tabs"},
    # Add a language dropdown into the admin
    "language_chooser": True,
}


JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": True,
    "brand_small_text": False,
    "brand_colour": False,
    "accent": "accent-primary",
    "navbar": "navbar-dark",
    "no_navbar_border": False,
    "navbar_fixed": True,
    "layout_boxed": False,
    "footer_fixed": True,
    "sidebar_fixed": True,
    "sidebar": "sidebar-dark-primary",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": True,
    "sidebar_nav_compact_style": True,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": True,
    "theme": "default",
    "dark_mode_theme": None,
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success"
    }
}
