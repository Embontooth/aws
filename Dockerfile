FROM public.ecr.aws/lambda/python:3.11

COPY lambda_function.py ${LAMBDA_TASK_ROOT}/
COPY requirements.txt ${LAMBDA_TASK_ROOT}/

# Install prebuilt binary wheels for the heavy packages first
RUN python3.11 -m pip install --upgrade pip wheel setuptools \
 && python3.11 -m pip install --only-binary=:all: numpy scikit-learn joblib \
 && python3.11 -m pip install -r ${LAMBDA_TASK_ROOT}/requirements.txt -t ${LAMBDA_TASK_ROOT}

# keep handler as before
CMD [ "lambda_function.lambda_handler" ]
