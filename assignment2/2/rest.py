import pandas as pd
from sklearn import svm
from random import randint
import numpy
from sklearn.metrics import classification_report, f1_score, accuracy_score, confusion_matrix

def most_common(lst):
    return max(set(lst), key=lst.count)

def most_pred(all_predictions):
    pred = []
    for i in range(len(all_predictions)):
        # ele = most_common(all_predictions[i])
        ele = all_predictions[i].index(min(all_predictions[i]))
        # if (ele == 2):
        #     ele = randint(-1,1)
        pred.append(ele-1)
    return pred

data = pd.read_csv('../assgnData/connect-4.csv', sep=',',header=None)

# no_vec = len(data)
no_vec = 1000

k_fold = 5
confusion = numpy.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]])

dt = [[0 for j in range(42*3)] for i in range(no_vec)]
dt_label = [0 for i in range(no_vec)]
for i in range(no_vec):
    if(data.loc[i,42]=='win'):
        dt_label[i] = 1
    elif(data.loc[i,42]=='loss'):
        dt_label[i] = -1
    elif(data.loc[i,42]=='draw'):
        dt_label[i] = 0

    for j in range(42):
        if(data.loc[i,j]=='o'):
            dt[i][3*j] = 1
        elif(data.loc[i,j]=='b'):
            dt[i][3*j+1] = 1
        elif(data.loc[i,j]=='x'):
            dt[i][3*j+2] = 1
# print(dt_label)

for i in range(k_fold):
    ti = int(i*no_vec/k_fold)
    tf = int((i+1)*no_vec/k_fold)
    ts_dataw = [] #win
    ts_datal = [] #loss
    ts_datad = [] #draw
    tr_dataw = []
    tr_datal = []
    tr_datad = []
    ts_lw = [] #win
    ts_ll = [] #loss
    ts_ld = [] #draw
    tr_lw = []
    tr_ll = []
    tr_ld = []
    for j in range(no_vec):
        if(j>=ti and j<tf):
            if(dt_label[j]==1):
                ts_dataw.append(dt[j])
                ts_lw.append(1)
            elif(dt_label[j]==-1):
                ts_datal.append(dt[j])
                ts_ll.append(-1)
            elif(dt_label[j]==0):
                ts_datad.append(dt[j])
                ts_ld.append(0)
        else:
            if(dt_label[j]==1):
                tr_dataw.append(dt[j])
                tr_lw.append(1)
            elif(dt_label[j]==-1):
                tr_datal.append(dt[j])
                tr_ll.append(-1)
            elif(dt_label[j]==0):
                tr_datad.append(dt[j])
                tr_ld.append(0)
    # print (tr_lw)
    # print (tr_ll)
    # print (tr_ld)

    clf1 = svm.SVC(kernel='linear') # Win
    tr_lrest = [2 for j in range(len(tr_ll+tr_ld))]
    clf1.fit(tr_dataw + tr_datal + tr_datad, tr_lw + tr_lrest)

    clf2 = svm.SVC(kernel='linear') # Loss
    tr_lrest = [2 for j in range(len(tr_lw+tr_ld))]
    clf2.fit(tr_datal + tr_dataw + tr_datad, tr_ll + tr_lrest)

    clf3 = svm.SVC(kernel='linear') # Draw
    tr_lrest = [2 for j in range(len(tr_ll+tr_lw))]
    clf3.fit(tr_datad + tr_datal + tr_dataw, tr_ld + tr_lrest)

    true_labels = ts_lw + ts_ll + ts_ld
    all_predictions = [[0,0,0] for j in range(ti,tf)]

    # pred1 = clf1.predict(ts_dataw + ts_datal + ts_datad)
    pred1 = clf1.decision_function(ts_dataw + ts_datal + ts_datad)
    # print (d)
    for j in range(0,tf-ti):
        all_predictions[j][2] = pred1[j]

    pred2 = clf2.decision_function(ts_dataw + ts_datal + ts_datad)
    for j in range(0,tf-ti):
        all_predictions[j][0] = pred2[j]

    pred3 = clf3.decision_function(ts_dataw + ts_datal + ts_datad)
    for j in range(0,tf-ti):
        all_predictions[j][1] = pred3[j]

    final_pred = most_pred(all_predictions)
    # print (all_predictions)
    print (classification_report(true_labels, final_pred))
    confusion += confusion_matrix(true_labels, final_pred)

print('Confusion matrix:')
print(confusion)
print ('row=expected, col=predicted')
