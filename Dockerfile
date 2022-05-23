FROM python
WORKDIR /tests_project
COPY . .
RUN pip install -r requirements.txt
ENV ENV=dev
CMD python -m pytest -vvs /tests_project/tests/