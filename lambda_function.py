import json
import boto3
import joblib
import os

# --- Load Model and Vectorizer from S3 ---
# This part assumes you already have logic to download/load your .pkl files.
# For example:
# s3 = boto3.client('s3')
# BUCKET_NAME = os.environ.get('BUCKET_NAME') # Set BUCKET_NAME in Lambda env vars
# s3.download_file(BUCKET_NAME, 'spam_model.pkl', '/tmp/spam_model.pkl')
# s3.download_file(BUCKET_NAME, 'tfidf_vectorizer.pkl', '/tmp/tfidf_vectorizer.pkl')
#
# model = joblib.load('/tmp/spam_model.pkl')
# vectorizer = joblib.load('/tmp/tfidf_vectorizer.pkl')
# --- (End of example model loading) ---

# For demonstration, we'll use placeholder logic.
# Replace this with your actual model loading.
print("Loading model and vectorizer...")
# model = ...
# vectorizer = ...


def lambda_handler(event, context):
    
    # Add a log to see exactly what Lambda receives
    print(f"Received event: {json.dumps(event)}")

    data = None
    
    try:
        # 1. Check if 'body' exists (from Function URL or API Gateway)
        if "body" in event and event["body"]:
            print("Parsing event['body']...")
            data = json.loads(event["body"])
        else:
            # 2. Assume event *is* the body (from a direct 'Test' invocation)
            print("Using event as data...")
            data = event
            
        # 3. Extract the email text
        email_text = data.get("text")

        if not email_text:
            print("Error: 'text' field is missing or empty in the request.")
            return {
                "statusCode": 400,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"error": "Empty text. Request body must be JSON with a 'text' key."})
            }

        print(f"Received text: {email_text}")

        # --- PREDICTION LOGIC ---
        # (Replace this with your actual scikit-learn logic)
        # 
        # Example:
        # 1. Vectorize the text
        # text_vectorized = vectorizer.transform([email_text])
        # 2. Predict
        # prediction_code = model.predict(text_vectorized)[0] # Get first prediction
        # result = "spam" if prediction_code == 1 else "ham"
        
        # Using a placeholder result for this example:
        result = "spam" if "free" in email_text.lower() else "ham"
        # --- END PREDICTION LOGIC ---

        print(f"Prediction: {result}")

        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({
                "text_processed": email_text,
                "prediction": result
            })
        }

    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from event body: {event.get('body')}")
        return {
            "statusCode": 400,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": "Invalid JSON format in request body."})
        }
    except Exception as e:
        # Catch other potential errors (e.g., model loading, prediction)
        print(f"Internal error: {str(e)}")
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": f"Internal server error: {str(e)}"})
        }