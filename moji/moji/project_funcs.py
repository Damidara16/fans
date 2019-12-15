def verify_following(f_user,c_user_uuid):
    return f_user.profile.following.filter(uuid=c_user_uuid).exists()

def upload_handler_chunk(f):
    fname = f'/media/new{f.name}'
    with open('new'+f.name, 'wb') as den:
        CHUNK_SIZE = 1024 * 5
        chunk = f.multiple_chunks(CHUNK_SIZE)
        while chunk:
            den.write(chunk)
            chunck = f.multiple_chunks(CHUNK_SIZE)
