import os
import json
from sklearn.metrics.pairwise import cosine_similarity


def calculate_features(interests_union:set, user:dict) -> list:
    """
    Returns a feature vector for a user

    Args:
     - interests_union (set): A union set that contains the interests in both users being compared
     - user (dict): A user dictionary object
    """
    feature = {}
    for interest in interests_union:
        feature[interest] = user['interests'][interest] if interest in user['interests'] else 0
    
    return list(feature.values())

def get_interests_union(user1:dict, user2:dict) -> set:
    """
    returns a union of the interests in both users
    """
    interests1 = set(user1['interests'])
    interests2 = set(user2['interests'])

    return interests1.union(interests2)

def get_feature_vectors(user1: dict, user2: dict) -> (list,list):
    """
    Calculate feature vector for both users
    """
    union_interests = get_interests_union(user1, user2)

    feature1 = calculate_features(union_interests,user1)
    feature2 = calculate_features(union_interests,user2)

    return feature1,feature2

def get_suggested_friends(my_user: int):
    """
    Get a list of the top 5 suggested friends for a given user id
    """

    #set the path for your database file
    
    path = os.path.join(os.getcwd(),os.path.dirname(__file__),"users.json")
    with open(path, 'r') as json_file:
        users = json.load(json_file)
    
    current_user = None
    similarities = []

    for user in users["users"]:
        if user['id'] == my_user:
            current_user = user
    
    if not current_user:
        raise KeyError(f"User with id {my_user} not in database")
    
    for user in users["users"]:

        if user == current_user:
            continue

        my_user_feature, friends_feature = get_feature_vectors(current_user,user)
        similarity = cosine_similarity([my_user_feature], [friends_feature])[0][0]
        similarities.append((user, similarity))
    
    similarities.sort(key=lambda x: x[1], reverse=True)
    recommendations = [user[0] for user in similarities[:5]]

    return recommendations


if __name__ == "__main__":
    print(get_suggested_friends(2))