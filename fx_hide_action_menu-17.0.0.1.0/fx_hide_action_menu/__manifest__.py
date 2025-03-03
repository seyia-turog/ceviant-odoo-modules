{
    "name": "Hide Action Menu",
    "summary": "Hide Action Menu",
    "version": "17.0.0.1.0",
    "description": """Hide Action Menu""",
    "author": "Doan Thanh Sang",
    "category": "Extra Tools",
    "license": "LGPL-3",
    "depends": ["base", "web"],
    "data": [
        "views/inherit_res_users_view.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "fx_hide_action_menu/static/src/**/*",
        ]
    },
    "installable": True,
    "auto_install": False,
    "application": True,
    "images": [
        "static/description/icon.png",
    ],
}
