# Dockerfile - use public Lambda Python 3.11 base
FROM public.ecr.aws/lambda/python:3.11

# Work in Lambda task root (this is where lambda runtime looks for handler by default)
WORKDIR ${LAMBDA_TASK_ROOT}

# Copy your handler and requirements
COPY lambda_function.py ${LAMBDA_TASK_ROOT}/
COPY requirements.txt ${LAMBDA_TASK_ROOT}/

# Upgrade pip, wheel, setuptools and install binary wheels for the heavy stuff first.
# These versions are known to have manylinux wheels for CPython 3.11:
#   numpy 2.2.6, scipy 1.16.3, scikit-learn 1.7.2, joblib 1.5.2
# Adjust versions if you want but make sure wheels exist.
RUN python3.11 -m pip install --upgrade pip wheel setuptools \
 && python3.11 -m pip install --only-binary=:all: \
      numpy==2.2.6 scipy==1.16.3 scikit-learn==1.7.2 joblib==1.5.2 \
 && python3.11 -m pip install --no-deps -r ${LAMBDA_TASK_ROOT}/requirements.txt -t ${LAMBDA_TASK_ROOT}

# Make sure the handler name matches your file/handler function
CMD ["lambda_function.lambda_handler"]
