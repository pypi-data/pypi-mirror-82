# villaProductSdk
> read and write product information in real time


## Install

`pip install villaProductSdk`

## How to use

Uploading a large amount of data using s3

## generate dummy data for testing

```python
#Dummy Data
sampleInput = {
  "message": "helloWorld",
  "roomId": 'C9ba1d024ed36979222a2a2a8f67cfc9a' ,
  "accessKey": accessKey
}

```

## Create main class object

```python
from linesdk.linesdk import Line

line = Line(accessKey = sampleInput['accessKey'] )
```

## send message

```python
%%time
line.send(message = sampleInput['message'])
```

## LambdaFunction

```python
%%time
line.lambdaSend(sampleInput, _)
```
