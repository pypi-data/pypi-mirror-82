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
line.send(roomId = sampleInput['roomId'] ,message = sampleInput['message'])
```

    CPU times: user 17.3 ms, sys: 5.13 ms, total: 22.4 ms
    Wall time: 352 ms





    True



## LambdaFunction

```python
%%time
line.lambdaSend(sampleInput, _)
```

    CPU times: user 12.8 ms, sys: 1.92 ms, total: 14.7 ms
    Wall time: 409 ms


# Call a deployed lambda function

```python
%%time
lineLambda = LineLambda(USER, PW)
lineLambda.send(message='hello', roomId = sampleInput['roomId'])
```
