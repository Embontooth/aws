import json
import boto3
import joblib
import os

# CONFIG
S3_BUCKET = "spam-detection-bucket-1"   # only used if models not in image
CLASSIFIER_KEY = "spam_model.pkl"
VECTORIZER_KEY = "tfidf_vectorizer.pkl"

LOCAL_CLASSIFIER_PATH = "/var/task/spam_model.pkl"       # when bundled in image
LOCAL_VECTORIZER_PATH = "/var/task/tfidf_vectorizer.pkl"

MODEL_LOADED = False
classifier = None
vectorizer = None

def load_models():
    global MODEL_LOADED, classifier, vectorizer
    if MODEL_LOADED:
        return

    # 1) try local files (bundled into image)
    if os.path.exists(LOCAL_CLASSIFIER_PATH) and os.path.exists(LOCAL_VECTORIZER_PATH):
        classifier = joblib.load(LOCAL_CLASSIFIER_PATH)
        vectorizer = joblib.load(LOCAL_VECTORIZER_PATH)
        MODEL_LOADED = True
        print("Loaded models from image filesystem")
        return

    # 2) fallback: download from S3 at runtime
    s3 = boto3.client("s3")
    clf_tmp = "/tmp/spam_model.pkl"
    vec_tmp = "/tmp/tfidf_vectorizer.pkl"
    if not os.path.exists(clf_tmp):
        s3.download_file(S3_BUCKET, CLASSIFIER_KEY, clf_tmp)
        s3.download_file(S3_BUCKET, VECTORIZER_KEY, vec_tmp)
    classifier = joblib.load(clf_tmp)
    vectorizer = joblib.load(vec_tmp)
    MODEL_LOADED = True
    print("Downloaded models from S3 into /tmp")

# handler
def lambda_handler(event, context):
    try:
        if not MODEL_LOADED:
            load_models()

        body = event.get("body")
        if isinstance(body, str):
            body = json.loads(body)
        text = body.get("text", "")
        if not text.strip():
            return {"statusCode":400, "body": json.dumps({"error":"Empty text"})}

        X = vectorizer.transform([text])
        pred = classifier.predict(X)[0]
        result = "SPAM" if int(pred) == 1 else "NOT SPAM"
        return {
            "statusCode":200,
            "headers":{"Access-Control-Allow-Origin":"*"},
            "body": json.dumps({"result": result})
        }
    except Exception as e:
        print("ERROR", e)
        return {"statusCode":500, "body": json.dumps({"error": str(e)})}
