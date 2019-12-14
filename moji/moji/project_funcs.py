
def verify_following(f_user,c_user_uuid):
    return f_user.profile.following.filter(uuid=c_user_uuid).exists()
