![Python package](https://github.com/cdaudt/pipeline/workflows/Python%20package/badge.svg)

# Simple data processing pipelines

Create simple data pipelines with sink/source modules that can 
process or drop elements. Each pipeline step receives a dictionary
of metadata+data for the element, and it can add/remove fields
to the element, or terminate processing of the element.

An example pipeline would be a generator (the **source**) which reads image files from a directory, followed by a pipe that resizes each image, followed by a pipe that saves each image. 
# Stages

Each stage can contain a **source**, a **sink**, or both. Sources generate elements, while sinks process and optionally drop elements from the pipeline.

## Source Stage

A source stage is defined by creating a subclass of 'Pipeline' class with a 'source' function at a minimum, as the example below.

```python
class ArraySource(pipeline.Pipeline):
    def __init__(self, sink, arr):
        self.arr = arr
        super(ArraySource, self).__init__(sink)

    def source(self):
        for i in range(len(self.arr)):

            element = {
                "word_id": i,
                "word": self.arr[i]
            }

            yield (element)
```
## Sink Stage
A sink stage is define by creating a subclass of 'Pipeline' class with a sink function at a minimum, as in the example below
```python
class DropSmallWord(pipeline.Pipeline):
    def __init__(self, sink, min):
        self.min = min
        super(DropSmallWord, self).__init__(sink)

    def sink(self, element):
        if len(element['word']) < self.min:
            return None
        else:
            return element

```

# Elements

Elements are the units of data passed through the processing pipeline. An element is a dictionary that can contain any number of fields. Both data and meta-data about the data unit can be contained in the element.

# Creating the Pipeline
In order to create a pipeline, the stages are created and linked to each other, starting from the final stage and working back to the source, as follows:
```python
    pw = PrintWord(None) # Save image
    ds = DropSmallWord(pw, 5)
    a = ArraySource(ds, words)
```
As can be seen, the final stage is initiated with ```None``` as sink, while all other stages receive their subsequent stage as sink

# Examples
Look in the examples subdirectory for these examples
   * feeder.py: Feeds an array of words into a filter stage that drops small words, followed by a stage that prints the remaining words
   * resizer.py: Reads image files from the command-line, passes them through a resizer stage, followed by an image-save stage.


