FROM public.ecr.aws/lambda/python:3.11

# Install build tools and libraries needed for numpy/scipy/scikit-learn
# (this increases image size and build time)
USER root
RUN yum -y update && \
    yum -y install gcc gcc-c++ make gfortran \
                   lapack-devel blas-devel openblas-devel \
                   python3-devel && \
    yum -y clean all

# Create working dir (Lambda runtime expects code in /var/task)
WORKDIR /var/task

# Copy handler and requirements into the image
COPY lambda_function.py ${LAMBDA_TASK_ROOT}/
COPY requirements.txt ${LAMBDA_TASK_ROOT}/

# Upgrade pip then install Python packages into the Lambda task root
RUN python3.11 -m pip install --upgrade pip wheel setuptools \
 && python3.11 -m pip install -r ${LAMBDA_TASK_ROOT}/requirements.txt -t ${LAMBDA_TASK_ROOT}

# Copy models (we downloaded these into the build context in CodeBuild)
COPY spam_model.pkl ${LAMBDA_TASK_ROOT}/spam_model.pkl
COPY tfidf_vectorizer.pkl ${LAMBDA_TASK_ROOT}/tfidf_vectorizer.pkl

# Use the default CMD for the python lambda base image
CMD ["lambda_function.lambda_handler"]
