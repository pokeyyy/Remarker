import pickle

labels = []
with open('C:/Users/pokey/Desktop/H2_Block_1_label.pkl', 'rb') as file:
    labels = pickle.load(file)

print(type(labels))
print(labels[0].shape)