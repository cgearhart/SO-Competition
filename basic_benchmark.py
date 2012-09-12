import competition_utilities as cu
import features
import preprocess
from sklearn.ensemble import RandomForestClassifier

# submission format:
# id(opt),not a real question,not constructive,off topic,open,too localized
# excpet for id, each column should be a value [0,1], while the sum of each row
# should be 1.

train_file = "train-sample.csv"
full_train_file = "train.csv"
test_file = "public_leaderboard.csv"
submission_file = "gearley.csv"

# default feature names could include things like 'userid', 'PostCreationDate',
# and the other column titles from the data itself 

feature_names = [ "OwnerUndeletedAnswerCountAtPostTime"
                , "ReputationAtPostCreation"
                , "TitleLength"
                , "UserAge"
                ]

code_functions = [ "NumLinesCode"
                 ]
text_functions = [ "NumParagraphs"
                 , "NumSentences"
                 , "LenSentences"
                 ]

def main():
    print("Reading the data")
    data = cu.get_dataframe(train_file)
    
    print("Preprocessing")
    code = preprocess.get_code(data)
    text = preprocess.get_text(data)
    codeFea = preprocess.process_and_pickle(code_functions,code,"training")
    textFea = preprocess.process_and_pickle(text_functions,text,"training")

    print("Extracting features")
    fea = features.extract_features(feature_names, data)
    
    print("Joining features")
    fea = fea.join(codeFea)
    fea = fea.join(textFea)

    print("Training the model")
    # n_estimators = 50 means "create 50 decision trees in the forest"
    # n_jobs = -1 means "automatically detect cores/threads and parallelize the job"
    rf = RandomForestClassifier(n_estimators=100, verbose=2, compute_importances=True, n_jobs=-1) # This just creates the object - nothing else happens
    rf.fit(fea, data["OpenStatus"]) # This line trains the classifier; it fits the data, mapped to features, to the classifier
    # training the classifier means minimizing gini impurity (by default)
    # look it up on Wikipedia (if you care)

    print("Reading test file and making predictions")
    data = cu.get_dataframe(test_file)
    
    code = preprocess.get_code(data)
    text = preprocess.get_text(data)
    codeFea = preprocess.process_and_pickle(code_functions,code,"Test")
    textFea = preprocess.process_and_pickle(text_functions,text,"Test")
    
    test_features = features.extract_features(feature_names, data)
    
    test_features = test_features.join(codeFea)
    test_features = test_features.join(textFea)
    
    probs = rf.predict_proba(test_features) # the predicted probabilities;
    # the values are usually called yHat in ML texts, the probabilities are the
    # measure of how likely it is that the output will take on the value yHat

    print("Calculating priors and updating posteriors")
    new_priors = cu.get_priors(full_train_file)
    old_priors = cu.get_priors(train_file)
    probs = cu.cap_and_update_priors(old_priors, probs, new_priors, 0.001)
    
    print("Saving submission to %s" % submission_file)
    cu.write_submission(submission_file, probs)

if __name__=="__main__":
    main()