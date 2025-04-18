import pandas as pd

train = pd.read_csv("C:/ML-Credit/credit card fraud detection/py/fraudTrain.csv", index_col=0)
test = pd.read_csv("C:/ML-Credit/credit card fraud detection/py/fraudTest.csv", index_col=0)

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, roc_curve, auc, accuracy_score
import matplotlib.pyplot as plt
import seaborn as sns


train['trans_date_trans_time'] = pd.to_datetime(train['trans_date_trans_time'])
train['hour'] = train['trans_date_trans_time'].dt.hour
train['minute'] = train['trans_date_trans_time'].dt.minute
train['second'] = train['trans_date_trans_time'].dt.second
train['year'] = train['trans_date_trans_time'].dt.year
train['month'] = train['trans_date_trans_time'].dt.month
train['day'] = train['trans_date_trans_time'].dt.day


features = ['amt', 'lat', 'long', 'city_pop', 'hour', 'minute', 'second', 'year', 'month', 'day']
X = train[features]
y = train['is_fraud']


X_train, X_valid, y_train, y_valid = train_test_split(X, y, test_size=0.2, random_state=42)


rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)
importances = rf_model.feature_importances_
indices = (-importances).argsort()[:5]

print("Top 5 Feature Importances:")
for i, index in enumerate(indices, 1):
    print(f"{i}. Feature {index}: {importances[index]}")


y_pred = rf_model.predict(X_valid)


cm = confusion_matrix(y_valid, y_pred)


fpr, tpr, thresholds = roc_curve(y_valid, rf_model.predict_proba(X_valid)[:, 1])
roc_auc = auc(fpr, tpr)


plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='g', cmap=sns.color_palette("Blues"), xticklabels=['Not Fraud', 'Fraud'], yticklabels=['Not Fraud', 'Fraud'], annot_kws={'size': 14})
plt.xlabel('Predicted', fontsize=14)
plt.ylabel('True', fontsize=14)
plt.title('Confusion Matrix', fontsize=16)
plt.show()


plt.figure(figsize=(8, 8))
plt.plot(fpr, tpr, color='darkorange', lw=2, label='ROC curve (area = {:.2f})'.format(roc_auc))
plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver Operating Characteristic (ROC) Curve')
plt.legend(loc='lower right')
plt.show()

from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        
        amt = float(request.form['amt'])
        lat = float(request.form['lat'])
        long = float(request.form['long'])
        city_pop = int(request.form['city_pop'])
        hour = int(request.form['hour'])
        minute = int(request.form['minute'])
        second = int(request.form['second'])
        year = int(request.form['year'])
        month = int(request.form['month'])
        day = int(request.form['day'])

        
        new_data = pd.DataFrame({
            'amt': [amt],
            'lat': [lat],
            'long': [long],
            'city_pop': [city_pop],
            'hour': [hour],
            'minute': [minute],
            'second': [second],
            'year': [year],
            'month': [month],
            'day': [day],
        })

        prediction = rf_model.predict(new_data)

        
        return render_template('index.html', prediction=prediction[0])

    
    return render_template('index.html', prediction=None)

if __name__ == '__main__':
    app.run(debug=True)