import portablemc



def get_startup_options(authsession_or_username, resolution=None):
    opts = portablemc.StartOptions()
    opts.resolution = resolution if resolution else (1366,768)
    if isinstance(authsession_or_username, str):
        opts.username = authsession_or_username
    else:
        opts.auth_session = authsession_or_username
