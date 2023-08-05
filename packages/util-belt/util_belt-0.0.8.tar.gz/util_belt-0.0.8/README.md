## utility belt
This is a utility package which can simplify a lot of common and repetitive tasks.<br/>
It contains different utility functions.</br>
to install it use ``` pip install util-belt ``` and `pip` will install the latest version of the package<br/>
### List of functionalities
1. ### file utilities
   1. list to text  <br/> to save a list to text file for later use you can do it using the <br/>
   ```list_to_txt()``` funtion in the `file_utils` module.
      #### example
      ```
      from util_belt.file_utils import list_to_txt

      my_list = [3,5,6,7]
      list_to_txt(my_list , file_dest = './list.txt')

      ```
      `file_dest` parameter is the file path where the list should be saved at. </br>
      By default it is  the current directory and the file name is `list.txt` <br>
      you can change that to any file path you want. the funtion will save your list <br>
      to a file with out worrying about details in file handling.<br>

      **Currently this library can only save simple lists or 1D lists**
   1. file from list</br>
      to get a list saved in a txt file use ``` list_from_txt ``` function in the ``` file_utils ``` module <br/>

      #### Example
      ```
      from util_belt.file_utils import list_from_txt

      my_list = list_from_txt('Documents/my_list.txt')

      ```
   **Currently this library can only save and retrieve simple lists or 1D lists.<br/> it will inlude more flexiblity and functionalities in the next update** <br/>
2. ### display utilities
   1. pretty print an array <br/>
      this functionality could be accessd at the `display_util` module<br/>
      it helps us print a numpy array beatifuly 
      ### Example
      ```
      from util_belt.display_utils import pretty_array
      three_d_array = np.random.randint(0, 10, size=(2,7,12))

      pretty_array(three_d_array,colorify = False,axis=0)
      ```
      The `colorify` parameter determines if the display should be colorful (by default it is flase). <br/>
      The `axis` parameter determines on which axis of the array should the different
      bands of color applied(by defualt it is 0).
      the out put from the above example looks like as follows:

<pre>
      / 6 0 4 3 5 8 4 7 9 1 4 3 /
     / 9 6 2 1 0 6 4 3 4 9 4 6 /
    / 6 3 5 1 4 9 8 9 9 0 8 4 /
   / 5 7 3 6 9 9 6 7 1 6 4 5 /
  / 6 2 1 6 5 6 4 0 8 9 1 2 /
 / 7 2 6 7 0 1 4 7 5 0 7 7 /

       / 7 3 5 1 5 7 2 4 5 6 1 5 /
      / 9 2 2 1 5 6 5 2 4 4 6 9 /
     / 4 1 6 8 6 0 2 6 8 4 0 7 /
    / 3 8 9 3 9 8 9 7 8 1 8 8 /
   / 4 5 7 7 0 5 4 5 5 1 4 7 /
  / 9 6 1 6 2 5 8 8 4 9 5 2 /
 / 7 2 8 2 7 7 3 4 3 1 0 9 /
</pre>
The origin or the `[0][0][0]` in this display starts from the bottom left corner.<br/>
Then the first axis (height) increases from bottom to top (like a Z axis in typical 3D cartesian plane)<br/>
The second axis (rows) increases away from the origin point along the diagonal line<br>
The third axis (columns) increases horizentaly to the right.<br>
This can be shown in the diagram below<br>
<pre>
first axis

|    second axis
|   /
|  /
| /
|/_________ third axis

</pre>

   if there is any issue,a bug or recommendation report on  https://github.com/kellemNegasi/util_belt
