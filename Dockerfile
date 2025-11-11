FROM public.ecr.aws/lambda/python:3.11

# Copy handler
COPY lambda_function.py ${LAMBDA_TASK_ROOT}/
# Copy requirements and install
COPY requirements.txt ${LAMBDA_TASK_ROOT}/
RUN python3.11 -m pip install --upgrade pip \
 && python3.11 -m pip install -r ${LAMBDA_TASK_ROOT}/requirements.txt -t ${LAMBDA_TASK_ROOT}

# Copy model files into image (if Build copied them into workspace)
# Build step will download model files to the repo folder before docker build
COPY spam_model.pkl ${LAMBDA_TASK_ROOT}/spam_model.pkl
COPY tfidf_vectorizer.pkl ${LAMBDA_TASK_ROOT}/tfidf_vectorizer.pkl

CMD ["lambda_function.lambda_handler"]
