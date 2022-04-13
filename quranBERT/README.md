# quranBERT ​
### in this folder we include one of the approachs we used for Quran QA task which we name quranBERT
the idea was to train general Masked Language Model that is fine tuned on quran only to be more familiar with the quranic verses (sentences ) to perform better in the question answering task 
to acheive this wwe go through four main steps :
1. preparing data : 
 - As described in the `quran preprocessing.ipynb` note book we used the data from kaggle [The Holy Quran](https://www.kaggle.com/datasets/zusmani/the-holy-quran) competition 
 - we normalize all diacritics (tashkeel ) and stopping signs (علامات الوقف ) 
 - transform all to .txt file (`quran.txt`) to be ready for training the model 
2. training araBERT for MLM on quran only 
 - in the `quranBERT.ipynb` notebook we use the preprocessed data for fine tuning [araBERT](https://huggingface.co/aubmindlab/bert-base-arabertv02) to quranic MLM 
3. train quranBERT for quran question answering 
 - fine tuning the quranBERT we made to question answering in `quran qa.ipynb` notebook
 - all team members used versions of this notebook for different trails but in this approach we used QuranQA competition data with our quran data for most of trails and in some trails we added random sample from arabic SQUAD data 
4. emseble many quranBERTs for better resutls 
 - we ensembled many trained models those models are different by the data used for training them and some of them only differ in number of (epochs , batch sizes , lr , weight decay) 
