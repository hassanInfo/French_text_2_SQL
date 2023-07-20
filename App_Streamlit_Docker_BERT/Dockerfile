FROM python:3.10.9
WORKDIR /app
COPY requirements.txt ./requirements.txt 
RUN pip install -r requirements.txt
RUN python -m spacy download fr_core_news_md
EXPOSE 8501
COPY . /app
ENTRYPOINT [ "streamlit", "run" ]
CMD ["app.py"]
