
def get_user_messages(array, user_name):
    result = []
    for line in array:
        if line[2] == user_name:
            result.append(line)
    return result