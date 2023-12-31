import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from numpy import array
from sklearn.neighbors import KNeighborsRegressor
from sklearn import svm
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_absolute_percentage_error
import altair as alt
import pickle


Data,Preproses,Modelling,Implementasi = st.tabs(['Data','Preprosessing Data','Modelling','Implementasi'])

with Data:
   st.title("""
   Peramalan Data Time Series Pada Saham PT Bank Central Asia Tbk.
   """)
   st.write('Proyek Sain Data')
   st.text("""
            1. Mohammad Zainal Taufik 200411100167 
            2. Gio Alpin Jeisa Tarigan 200411100199   
            """)
   st.subheader('Tentang Dataset')
   st.write ("""
   Data yang kami gunakan adalah data time series pada Saham PT Bank Central Asia Tbk, datanya diambil dari sumber yang tersedia secara publik. Anda dapat mengakses data tersebut melalui tautan berikut ini.
   https://finance.yahoo.com/quote/BBCA.JK/history?p=BBCA.JK
   """)
   st.write ("""
    Berikut adalah deskripsi atribut pada dataset yang digunakan, yang terdiri dari 248 data:
    """)
   st.write('1. Tanggal (Date): Merupakan tanggal perdagangan mulai dari tanggal 15 Juni 2022 hingga 15 Juni 2023.')
   st.write('2. Harga Pembukaan (Open): Menyimpan harga saham pada saat pembukaan perdagangan pada setiap hari.')
   st.write('3. Harga Tertinggi (High): Menyimpan harga tertinggi yang dicapai oleh saham pada setiap hari.')
   st.write('4. Harga Terendah (Low): Menyimpan harga terendah yang dicapai oleh saham pada setiap hari.')
   st.write('5. Harga Penutupan (Close): Menyimpan harga saham pada saat penutupan perdagangan pada setiap hari.')
   st.write('6. Harga Penutupan yang Disesuaikan (Adj. Close): Menyimpan harga penutupan saham yang telah disesuaikan dengan aksi korporasi seperti right issue, stock split, atau stock reverse.')
   st.write('7. Volume Perdagangan (Volume): Menyimpan volume perdagangan saham dalam satuan lembar.')
   st.subheader('Dataset')
   df = pd.read_csv('bca.csv')
   df
   st.write('Dilakukan Pengecekan data kosong (Missing Value)')
   st.write(df.isnull().sum())
   st.write('Masih Terdapat data kosong maka dilakukan penanganan dengan mengisinya dengan nilai median')
   df['Open'] = df['Open'].fillna(value=df['Open'].median())
   df['High'] = df['High'].fillna(value=df['High'].median())
   df['Low'] = df['Low'].fillna(value=df['Low'].median())
   df['Close'] = df['Close'].fillna(value=df['Close'].median())
   df['Adj Close'] = df['Adj Close'].fillna(value=df['Adj Close'].median())
   df['Volume'] = df['Volume'].fillna(value=df['Volume'].median())
   st.write('Setelah dilakukan penanganan')
   st.write(df.isnull().sum())


with Preproses:
   # untuk mengambil data yang akan diproses
   data = df['Open']
   # menghitung jumlah data
   n = len(data)
   # membagi data menjadi 80% untuk data training dan 20% data testing
   sizeTrain = (round(n*0.8))
   data_train = pd.DataFrame(data[:sizeTrain])
   data_test = pd.DataFrame(data[sizeTrain:])
   st.write("""roses pembagian data menjadi 80% data training dan 20% data testing dilakukan untuk keperluan eksperimen dan evaluasi model.""")
   st.write("""Selanjutnya, dilakukan normalisasi data menggunakan teknik MinMax Scaler. Teknik ini digunakan untuk mengubah nilai-nilai pada dataset menjadi rentang yang lebih kecil antara 0 dan 1.""")
   min_ = st.checkbox('MinMax Scaler')
   mod = st.button("Cek")
   # melakukan normalisasi menggunakan minMaxScaler
   scaler = MinMaxScaler()
   train_scaled = scaler.fit_transform(data_train)
   # Mengaplikasikan MinMaxScaler pada data pengujian
   test_scaled = scaler.transform(data_test)
   # reshaped_data = data.reshape(-1, 1)
   train = pd.DataFrame(train_scaled, columns = ['data'])
   train = train['data']
   test = pd.DataFrame(test_scaled, columns = ['data'])
   test = test['data']
   if min_:
      if mod:
         st.write("Data Training MinMax Scaler")
         train
         st.write("Data Test MinMax Scaler")
         train

   def split_sequence(sequence, n_steps):
      X, y = list(), list()
      for i in range(len(sequence)):
         # find the end of this pattern
         end_ix = i + n_steps
         # check if we are beyond the sequence
         if end_ix > len(sequence)-1:
            break
         # gather input and output parts of the pattern
         seq_x, seq_y = sequence[i:end_ix], sequence[end_ix]
         X.append(seq_x)
         y.append(seq_y)
      return array(X), array(y)
   #memanggil fungsi untuk data training
   df_X, df_Y = split_sequence(train, 4)
   x = pd.DataFrame(df_X, columns = ['xt-4','xt-3','xt-2','xt-1'])
   y = pd.DataFrame(df_Y, columns = ['xt'])
   dataset_train = pd.concat([x, y], axis=1)
   dataset_train.to_csv('data-train.csv', index=False)
   X_train = dataset_train.iloc[:, :4].values
   Y_train = dataset_train.iloc[:, -1].values
   #memanggil fungsi untuk data testing
   test_x, test_y = split_sequence(test, 4)
   x = pd.DataFrame(test_x, columns = ['xt-4','xt-3','xt-2','xt-1'])
   y = pd.DataFrame(test_y, columns = ['xt'])
   dataset_test = pd.concat([x, y], axis=1)
   dataset_test.to_csv('data-test.csv', index=False)
   X_test = dataset_test.iloc[:, :4].values
   Y_test = dataset_test.iloc[:, -1].values
with Modelling:

   def tuning(X_train,Y_train,X_test,Y_test,iterasi):
    hasil = 1
    iter = 0
    for i in range(1,iterasi):
        neigh = KNeighborsRegressor(n_neighbors=i)
        neigh = neigh.fit(X_train,Y_train)
        y_pred=neigh.predict(X_test)
        reshaped_data = y_pred.reshape(-1, 1)
        original_data = scaler.inverse_transform(reshaped_data)
        reshaped_datates = Y_test.reshape(-1, 1)
        actual_test = scaler.inverse_transform(reshaped_datates)
        akhir1 = pd.DataFrame(original_data)
        akhir = pd.DataFrame(actual_test)
        mape = mean_absolute_percentage_error(original_data, actual_test)
        if mape < hasil:
            hasil = mape
            iter = i
    return hasil, iter
   akr,iter = tuning(X_train,Y_train,X_test,Y_test,30)
   # Model knn
   neigh = KNeighborsRegressor(n_neighbors=2)
   neigh.fit(X_train,Y_train)
   y_pred=neigh.predict(X_test)
   reshaped_data = y_pred.reshape(-1, 1)
   original_data = scaler.inverse_transform(reshaped_data)
   reshaped_datates = Y_test.reshape(-1, 1)
   actual_test = scaler.inverse_transform(reshaped_datates)
   akhir1 = pd.DataFrame(original_data)
   akhir1.to_csv('prediksi.csv', index=False)
   akhir = pd.DataFrame(actual_test)
   akhir.to_csv('aktual.csv', index=False)
   mape_knn = mean_absolute_percentage_error(original_data, actual_test)

   # Model svm
   clf_svm = svm.SVR(kernel='rbf')
   clf_svm.fit(X_train,Y_train)
   y_pred_SVM=clf_svm.predict(X_test)
   reshaped_data_SVM = y_pred_SVM.reshape(-1, 1)
   original_data_ = scaler.inverse_transform(reshaped_data_SVM)
   reshaped_datates_ = Y_test.reshape(-1, 1)
   actual_test_ = scaler.inverse_transform(reshaped_datates_)
   mape_svm = mean_absolute_percentage_error(original_data_, actual_test_)

   # Model dtr
   regressor = DecisionTreeRegressor()
   regressor.fit(X_train, Y_train)
   y_pred_dtr=regressor.predict(X_test)
   reshaped_data = y_pred_dtr.reshape(-1, 1)
   _original_data = scaler.inverse_transform(reshaped_data)
   reshaped_datates = Y_test.reshape(-1, 1)
   _actual_test = scaler.inverse_transform(reshaped_datates)
   mape_dtr = mean_absolute_percentage_error(_original_data, _actual_test)

   st.subheader("Berikut adalah beberapa pilihan model yang tersedia!")
   st.write("Silakan pilih model yang ingin Anda gunakan untuk memeriksa MAPE")
   kn = st.checkbox('K-Nearest Neighbor')
   svm_ = st.checkbox('Supper Vector Machine')
   des = st.checkbox('Decision Tree')
   mod = st.button("Mulai Pemodelan")


   if kn :
      if mod:
         st.write('Model KNN Menghasilkan Mape: {}'. format(mape_knn))
   if svm_ :
      if mod:
         st.write("Model SVM Menghasilkan Mape : {}" . format(mape_svm))
   if des :
      if mod:
         st.write("Model Decision Tree Menghasilkan Mape : {}" . format(mape_dtr))
   
   eval = st.button("Evaluasi semua model")
   if eval :
      # st.snow()
      source = pd.DataFrame({
            'Nilai Mape' : [mape_knn,mape_svm,mape_dtr],
            'Nama Model' : ['KNN','SVM','Decision Tree']
      })
      bar_chart = alt.Chart(source).mark_bar().encode(
            y = 'Nilai Mape',
            x = 'Nama Model'
      )
      st.altair_chart(bar_chart,use_container_width=True)



with Implementasi:
   #menyimpan model
   with open('knn','wb') as r:
      pickle.dump(neigh,r)
   with open('minmax','wb') as r:
      pickle.dump(scaler,r)
   
   st.title("""Implementasi Data""")
   input_1 = st.number_input('Nilai Pertama')
   input_2 = st.number_input('Nilai Kedua')
   input_3 = st.number_input('Nilai Ketiga')
   input_4 = st.number_input('Nilai Keempat')

   def submit():
      # inputs = np.array([inputan])
      with open('knn', 'rb') as r:
         model = pickle.load(r)
      with open('minmax', 'rb') as r:
         minmax = pickle.load(r)
      data1 = minmax.transform([[input_1]])
      data2 = minmax.transform([[input_2]])
      data3 = minmax.transform([[input_3]])
      data4 = minmax.transform([[input_4]])

      X_pred = model.predict([[(data1[0][0]),(data2[0][0]),(data3[0][0]),(data4[0][0])]])
      t_data1= X_pred.reshape(-1, 1)
      original = minmax.inverse_transform(t_data1)
      hasil =f"Prediksi Hasil Peramalan Pada Harga Pembukaan Saham PT Bank Central Asia Tbk. adalah: {original[0][0]}"
      st.success(hasil)

   all = st.button("Submit")
   if all :
      st.balloons()
      submit()

