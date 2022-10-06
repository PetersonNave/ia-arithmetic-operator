from mlforkids import MLforKidsImageProject

# treat this key like a password and keep it secret!
key = "0b9bc1f0-4446-11ed-9c85-e9175b095422a46f8bf5-ac45-4c45-8d5e-344a7aa7139e"

# this will train your model and might take a little while
myproject = MLforKidsImageProject(key)
myproject.train_model()

# CHANGE THIS to the image file you want to recognize
demo = myproject.prediction("my-test-image.jpg")

label = demo["class_name"]
confidence = demo["confidence"]

# CHANGE THIS to do something different with the result
print ("result: '%s' with %d%% confidence" % (label, confidence))

demo = myproject.prediction("my-test-image2.jpg")

label = demo["class_name"]
confidence = demo["confidence"]

# CHANGE THIS to do something different with the result
print ("result: '%s' with %d%% confidence" % (label, confidence))
demo = myproject.prediction("my-test-image3.jpg")

label = demo["class_name"]
confidence = demo["confidence"]

# CHANGE THIS to do something different with the result
print ("result: '%s' with %d%% confidence" % (label, confidence))