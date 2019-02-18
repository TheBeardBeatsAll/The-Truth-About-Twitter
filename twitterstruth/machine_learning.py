import os
import django
import numpy as np
import random
from sklearn.model_selection import KFold, cross_val_score
from sklearn.naive_bayes import BernoulliNB


# Ensure file when run separately can access models and settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'The_Truth_about_Twitter.settings')
django.setup()
from twitterstruth.models import Account


def get_accounts(dum_features, dum_targets, account_type, sample_size):
    # Get accounts of specified type and then get random sub-sample from it
    accounts = Account.objects.filter(account_type=account_type)
    random_accounts = random.sample(list(accounts), sample_size)

    # if not getattr(row, 'name'):
    #     no_name = 1
    # else:
    #     no_name = 0
    # if getattr(row, 'default_profile_image') == 1.0:
    #     default_prof_pic = 1
    # else:
    #     default_prof_pic = 0
    # if getattr(row, 'geo_enabled') != 1.0:
    #     no_geo_location = 1
    # else:
    #     no_geo_location = 0
    # if not getattr(row, 'description'):
    #     no_desc = 1
    # else:
    #     no_desc = 0
    # if friends < 30:
    #     lt_30_friends = 1
    #     gt_1000_friends = 0
    # elif friends > 1000:
    #     lt_30_friends = 0
    #     gt_1000_friends = 1
    # else:
    #     lt_30_friends = 0
    #     gt_1000_friends = 0
    # if getattr(row, 'statuses_count') == 0:
    #     never_tweeted = 1
    # else:
    #     never_tweeted = 0
    # if friends > 3 * getattr(row, 'followers_count'):
    #     three_friends_one_follower = 1
    # else:
    #     three_friends_one_follower = 0
    # Get database objects into list formats
    for acc in random_accounts:
        dum_features.append([acc.default_profile_pic, acc.gt_1000_friends,
                             acc.lt_30_friends, acc.never_tweeted,
                             acc.no_desc, acc.no_name, acc.not_geo_located,
                             acc.three_friends_one_followers])

        if acc.real_account:
            dum_targets.append(0)
        else:
            dum_targets.append(1)

    return dum_features, dum_targets


features = []
targets = []

features, targets = get_accounts(features, targets, 1, 1000)
features, targets = get_accounts(features, targets, 4, 1000)

# Convert lists to NumPy arrays
features = np.asarray(features)
targets = np.asarray(targets)

# Initialise classifier and k-fold cross validation
clf = BernoulliNB()
kf = KFold(n_splits=10, shuffle=True)

print('Data comprises of 2000 shuffled accounts:\n'
      '    1000 random Genuine accounts\n'
      '    1000 random Traditional accounts\n'
      'K-fold Cross validation used with k = 10\n'
      'Classifier: Naive Bayes with Bernoulli distribution\n'
      'Mean of the partition scores for each run:\n')

# Train and test model using k-fold cross validation 5 times and output mean scores
for index in range(5):
    scores = cross_val_score(estimator=clf, X=features, y=targets, cv=kf)
    print('    Run ' + str(index) + ': ' + str(np.mean(scores)))
