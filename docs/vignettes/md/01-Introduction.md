
# Introduction to petpy

This notebook introduces the `petpy` package and how to authenticate and interface with the Petfinder API. More information on the Petfinder API itself can be found on their [documentation page](https://www.petfinder.com/developers/api-docs#methods).

# Table of Contents

* [Installing petpy and Obtaining an API key](#installation)
* [Examples using the `petpy` package](#examples)
    - [Pet Methods](#petmethods)
        - [Extracting breeds of animals available in the Petfinder database](#breeds.list)
        - [Returning random Petfinder pet records](#pet.getRandom)
        - [Return a pet record associated with a specific petId](#pet.get)
        - [Finding pet records matching particular search criteria](#pet.find)
    - [Shelter Methods](#sheltermethods)
        - [Finding shelters matching search criteria](#shelter.find)
        - [Returning specific shelter information](#shelter.get)
        - [Extracting pet records from a particular shelter](#shelter.getPets)
        - [Finding shelters that have records matching a particular animal breed](#shelter.listByBreed)

<a id='installation'></a>

## Installation

If not already installed, install `petpy` using `pip`:

``pip install petpy``

Then, import the package.


```python
import petpy
```

The Petfinder API requires an API key to authenticate access. To receive an API key, register with Petfinder on their developer page: https://www.petfinder.com/developers/api-key

The API key received from Petfinder is then used to authenticate the `Petfinder` class in `petpy`.

The API key is first stored as an environment variable and then loaded using the `os` library. Storing your keys received from APIs and other sensitive information in a secure file or as an environment variable is considered best practice to avoid any potential malicious activity.


```python
import os

with open(os.path.join(os.getcwd(), 'api_key')) as k:
    key = k.read()
```


```python
pf = petpy.Petfinder(key)
```

The `pf` variable is the initialized Petfinder class with our given API key. We can now use this instance to interact with and extract data from the Petfinder API.

<a id='#examples'></a>

## Examples using the `petpy` package

<a id='petmethods'></a>

## Pet Methods

The following examples demonstrate some simple usage of using `petpy` to interact with and pull data from the Petfinder database. `petpy` contains methods for coercing the returned API results into a pandas DataFrame for easier data analysis and exporting the results into more common formats such as .csv or Excel. More examples of how to use `petpy` in conjunction with the Python scientific computing stack (Scipy, Numpy, pandas, scikit-learn, etc.) to analyze the results can be found in the later chapters of this introduction.

<a id='breed.list'></a>

### Getting Animal Breeds

Pulling the list of animal breeds from the Petfinder database is straightforward with `petpy`. Let's say we are interested in finding the available breeds of cats:


```python
cats = pf.breed_list('cat')
```

The default return format is JSON, but can be changed to XML by setting the default parameter `outputformat` to 'xml'.


```python
cats
```




    {'@encoding': 'iso-8859-1',
     '@version': '1.0',
     'petfinder': {'@xmlns:xsi': 'http://www.w3.org/2001/XMLSchema-instance',
      '@xsi:noNamespaceSchemaLocation': 'http://api.petfinder.com/schemas/0.9/petfinder.xsd',
      'breeds': {'@animal': 'cat',
       'breed': [{'$t': 'Abyssinian'},
        {'$t': 'American Curl'},
        {'$t': 'American Shorthair'},
        {'$t': 'American Wirehair'},
        {'$t': 'Applehead Siamese'},
        {'$t': 'Balinese'},
        {'$t': 'Bengal'},
        {'$t': 'Birman'},
        {'$t': 'Bobtail'},
        {'$t': 'Bombay'},
        {'$t': 'British Shorthair'},
        {'$t': 'Burmese'},
        {'$t': 'Burmilla'},
        {'$t': 'Calico'},
        {'$t': 'Canadian Hairless'},
        {'$t': 'Chartreux'},
        {'$t': 'Chausie'},
        {'$t': 'Chinchilla'},
        {'$t': 'Cornish Rex'},
        {'$t': 'Cymric'},
        {'$t': 'Devon Rex'},
        {'$t': 'Dilute Calico'},
        {'$t': 'Dilute Tortoiseshell'},
        {'$t': 'Domestic Long Hair'},
        {'$t': 'Domestic Long Hair (Black & White)'},
        {'$t': 'Domestic Long Hair (Black)'},
        {'$t': 'Domestic Long Hair (Brown)'},
        {'$t': 'Domestic Long Hair (Buff & White)'},
        {'$t': 'Domestic Long Hair (Buff)'},
        {'$t': 'Domestic Long Hair (Gray & White)'},
        {'$t': 'Domestic Long Hair (Gray)'},
        {'$t': 'Domestic Long Hair (Orange & White)'},
        {'$t': 'Domestic Long Hair (Orange)'},
        {'$t': 'Domestic Long Hair (White)'},
        {'$t': 'Domestic Medium Hair'},
        {'$t': 'Domestic Medium Hair (Black & White)'},
        {'$t': 'Domestic Medium Hair (Black)'},
        {'$t': 'Domestic Medium Hair (Brown)'},
        {'$t': 'Domestic Medium Hair (Buff & White)'},
        {'$t': 'Domestic Medium Hair (Buff)'},
        {'$t': 'Domestic Medium Hair (Gray & White)'},
        {'$t': 'Domestic Medium Hair (Gray)'},
        {'$t': 'Domestic Medium Hair (Orange & White)'},
        {'$t': 'Domestic Medium Hair (Orange)'},
        {'$t': 'Domestic Medium Hair (White)'},
        {'$t': 'Domestic Short Hair'},
        {'$t': 'Domestic Short Hair (Black & White)'},
        {'$t': 'Domestic Short Hair (Black)'},
        {'$t': 'Domestic Short Hair (Brown)'},
        {'$t': 'Domestic Short Hair (Buff & White)'},
        {'$t': 'Domestic Short Hair (Buff)'},
        {'$t': 'Domestic Short Hair (Gray & White)'},
        {'$t': 'Domestic Short Hair (Gray)'},
        {'$t': 'Domestic Short Hair (Mitted)'},
        {'$t': 'Domestic Short Hair (Orange & White)'},
        {'$t': 'Domestic Short Hair (Orange)'},
        {'$t': 'Domestic Short Hair (White)'},
        {'$t': 'Egyptian Mau'},
        {'$t': 'Exotic Shorthair'},
        {'$t': 'Extra-Toes Cat / Hemingway Polydactyl'},
        {'$t': 'Havana'},
        {'$t': 'Himalayan'},
        {'$t': 'Japanese Bobtail'},
        {'$t': 'Javanese'},
        {'$t': 'Korat'},
        {'$t': 'LaPerm'},
        {'$t': 'Maine Coon'},
        {'$t': 'Manx'},
        {'$t': 'Munchkin'},
        {'$t': 'Nebelung'},
        {'$t': 'Norwegian Forest Cat'},
        {'$t': 'Ocicat'},
        {'$t': 'Oriental Long Hair'},
        {'$t': 'Oriental Short Hair'},
        {'$t': 'Oriental Tabby'},
        {'$t': 'Persian'},
        {'$t': 'Pixie-Bob'},
        {'$t': 'Ragamuffin'},
        {'$t': 'Ragdoll'},
        {'$t': 'Russian Blue'},
        {'$t': 'Scottish Fold'},
        {'$t': 'Selkirk Rex'},
        {'$t': 'Siamese'},
        {'$t': 'Siberian'},
        {'$t': 'Silver'},
        {'$t': 'Singapura'},
        {'$t': 'Snowshoe'},
        {'$t': 'Somali'},
        {'$t': 'Sphynx / Hairless Cat'},
        {'$t': 'Tabby'},
        {'$t': 'Tabby (Black)'},
        {'$t': 'Tabby (Brown)'},
        {'$t': 'Tabby (Buff)'},
        {'$t': 'Tabby (Gray)'},
        {'$t': 'Tabby (Orange)'},
        {'$t': 'Tabby (White)'},
        {'$t': 'Tiger'},
        {'$t': 'Tonkinese'},
        {'$t': 'Torbie'},
        {'$t': 'Tortoiseshell'},
        {'$t': 'Turkish Angora'},
        {'$t': 'Turkish Van'},
        {'$t': 'Tuxedo'}]},
      'header': {'status': {'code': {'$t': '100'}, 'message': {}},
       'timestamp': {'$t': '2017-11-23T02:45:12Z'},
       'version': {'$t': '0.1'}}}}



The `return_df` parameter can also be set to True to coerce the results into a pandas DataFrame.


```python
cats_df = pf.breed_list('cat', return_df=True)
cats_df.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>cat breeds</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Abyssinian</td>
    </tr>
    <tr>
      <th>1</th>
      <td>American Curl</td>
    </tr>
    <tr>
      <th>2</th>
      <td>American Shorthair</td>
    </tr>
    <tr>
      <th>3</th>
      <td>American Wirehair</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Applehead Siamese</td>
    </tr>
  </tbody>
</table>
</div>



Please note the coercion to a pandas DataFrame removes the metadata returned in the JSON format to make the conversion process more efficient and straightforward.

According to Petfinder's API documentation, the available animals to search are ['barnyard', 'bird', 'cat', 'dog', 'horse', 'reptile', 'smallfurry']. Searching for an animal not available in the Petfinder database will return a JSON object with a message stating 'invalid arguments'.


```python
pf.breed_list('zebra')
```




    {'@encoding': 'iso-8859-1',
     '@version': '1.0',
     'petfinder': {'@xmlns:xsi': 'http://www.w3.org/2001/XMLSchema-instance',
      '@xsi:noNamespaceSchemaLocation': 'http://api.petfinder.com/schemas/0.9/petfinder.xsd',
      'header': {'status': {'code': {'$t': '200'},
        'message': {'$t': 'invalid arguments'}},
       'timestamp': {'$t': '2017-11-23T02:45:17Z'},
       'version': {'$t': '0.1'}}}}



<a id='pet.getRandom'></a>

### Returning random Petfinder pet records

The `petpy` method `pet_getRandom()` provides a wrapper for the Petfinder `pet.getRandom` method. The potential results can be filtered to a subset by the method parameters, otherwise the method can be called simply as:


```python
pf.pet_getRandom()
```




    {'@encoding': 'iso-8859-1',
     '@version': '1.0',
     'petfinder': {'@xmlns:xsi': 'http://www.w3.org/2001/XMLSchema-instance',
      '@xsi:noNamespaceSchemaLocation': 'http://api.petfinder.com/schemas/0.9/petfinder.xsd',
      'header': {'status': {'code': {'$t': '100'}, 'message': {}},
       'timestamp': {'$t': '2017-11-23T02:45:21Z'},
       'version': {'$t': '0.1'}},
      'petIds': {'id': {'$t': '35781395'}}}}



The default record output contains only the pet record's ID and the call's JSON metadata. If we wish to return a more complete random pet record, we can set the parameter `output` to `basic` (name, age, animal, breed, shelterID) or `full` (complete record with description).


```python
pf.pet_getRandom(output='full')
```




    {'@encoding': 'iso-8859-1',
     '@version': '1.0',
     'petfinder': {'@xmlns:xsi': 'http://www.w3.org/2001/XMLSchema-instance',
      '@xsi:noNamespaceSchemaLocation': 'http://api.petfinder.com/schemas/0.9/petfinder.xsd',
      'header': {'status': {'code': {'$t': '100'}, 'message': {}},
       'timestamp': {'$t': '2017-11-23T02:45:24Z'},
       'version': {'$t': '0.1'}},
      'pet': {'age': {'$t': 'Adult'},
       'animal': {'$t': 'Dog'},
       'breeds': {'breed': [{'$t': 'Chihuahua'}, {'$t': 'Terrier'}]},
       'contact': {'address1': {},
        'address2': {},
        'city': {'$t': 'Brazil'},
        'email': {'$t': 'luckypupsrescue@gmail.com'},
        'fax': {},
        'phone': {'$t': '(317) 443-2918'},
        'state': {'$t': 'IN'},
        'zip': {'$t': '47834'}},
       'description': {'$t': 'Nacho is an older dog who came to us from another rescue. He is very much a lap dog! he loves to ride in cars and even on the lawn mower! He is housebroken, neutered, up to date on shots, and will be microchipped once adopted. Send us an email at luckypupsrescue@gmail.com for more info!'},
       'id': {'$t': '39113649'},
       'lastUpdate': {'$t': '2017-08-15T16:30:40Z'},
       'media': {'photos': {'photo': [{'$t': 'http://photos.petfinder.com/photos/pets/39113649/1/?bust=1502814504&width=60&-pnt.jpg',
           '@id': '1',
           '@size': 'pnt'},
          {'$t': 'http://photos.petfinder.com/photos/pets/39113649/1/?bust=1502814504&width=95&-fpm.jpg',
           '@id': '1',
           '@size': 'fpm'},
          {'$t': 'http://photos.petfinder.com/photos/pets/39113649/1/?bust=1502814504&width=500&-x.jpg',
           '@id': '1',
           '@size': 'x'},
          {'$t': 'http://photos.petfinder.com/photos/pets/39113649/1/?bust=1502814504&width=300&-pn.jpg',
           '@id': '1',
           '@size': 'pn'},
          {'$t': 'http://photos.petfinder.com/photos/pets/39113649/1/?bust=1502814504&width=50&-t.jpg',
           '@id': '1',
           '@size': 't'}]}},
       'mix': {'$t': 'yes'},
       'name': {'$t': 'Nacho'},
       'options': {'option': [{'$t': 'hasShots'},
         {'$t': 'noKids'},
         {'$t': 'altered'},
         {'$t': 'housetrained'}]},
       'sex': {'$t': 'M'},
       'shelterId': {'$t': 'IN501'},
       'shelterPetId': {},
       'size': {'$t': 'S'},
       'status': {'$t': 'A'}}}}



We can also pull a specified number of pet records from the API by setting the `records` parameter and return the collected results as a pandas DataFrame by setting `return_df` to `True`.


```python
random_pet_df = pf.pet_getRandom(records=5, return_df=True)
```


```python
random_pet_df
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>age</th>
      <th>animal</th>
      <th>breed0</th>
      <th>breed1</th>
      <th>breeds.breed</th>
      <th>contact.address1</th>
      <th>contact.city</th>
      <th>contact.email</th>
      <th>contact.phone</th>
      <th>contact.state</th>
      <th>...</th>
      <th>photos9</th>
      <th>sex</th>
      <th>shelterId</th>
      <th>shelterPetId</th>
      <th>size</th>
      <th>status</th>
      <th>status0</th>
      <th>status1</th>
      <th>status2</th>
      <th>status3</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Senior</td>
      <td>Cat</td>
      <td>Domestic Short Hair</td>
      <td>NaN</td>
      <td>Domestic Short Hair</td>
      <td>4081 Columbia Avenue</td>
      <td>Columbia</td>
      <td>catmisonly2@yahoo.com</td>
      <td>717-684-2285</td>
      <td>PA</td>
      <td>...</td>
      <td>NaN</td>
      <td>M</td>
      <td>PA696</td>
      <td>NaN</td>
      <td>S</td>
      <td>A</td>
      <td>hasShots</td>
      <td>altered</td>
      <td>housetrained</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>0</th>
      <td>Adult</td>
      <td>Dog</td>
      <td>Chihuahua</td>
      <td>NaN</td>
      <td>Chihuahua</td>
      <td>NaN</td>
      <td>Romeoville</td>
      <td>info@perfectpooches.org</td>
      <td>NaN</td>
      <td>IL</td>
      <td>...</td>
      <td>http://photos.petfinder.com/photos/pets/397199...</td>
      <td>F</td>
      <td>IL753</td>
      <td>NaN</td>
      <td>S</td>
      <td>A</td>
      <td>hasShots</td>
      <td>altered</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>0</th>
      <td>Adult</td>
      <td>Cat</td>
      <td>Domestic Short Hair (Gray &amp; White)</td>
      <td>NaN</td>
      <td>Domestic Short Hair (Gray &amp; White)</td>
      <td>NaN</td>
      <td>Closter</td>
      <td>clawsadopt@yahoo.com</td>
      <td>(201) 768-0200</td>
      <td>NJ</td>
      <td>...</td>
      <td>http://photos.petfinder.com/photos/pets/386709...</td>
      <td>F</td>
      <td>NJ279</td>
      <td>Marcia</td>
      <td>M</td>
      <td>A</td>
      <td>hasShots</td>
      <td>altered</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>0</th>
      <td>Young</td>
      <td>Dog</td>
      <td>Labrador Retriever</td>
      <td>German Shepherd Dog</td>
      <td>NaN</td>
      <td>PO Box 421</td>
      <td>Ben Wheeler</td>
      <td>admin@vzchumanesociety.org</td>
      <td>903-962-5700</td>
      <td>TX</td>
      <td>...</td>
      <td>http://photos.petfinder.com/photos/pets/317327...</td>
      <td>M</td>
      <td>TX310</td>
      <td>8366590</td>
      <td>L</td>
      <td>A</td>
      <td>specialNeeds</td>
      <td>hasShots</td>
      <td>altered</td>
      <td>housetrained</td>
    </tr>
    <tr>
      <th>0</th>
      <td>Baby</td>
      <td>Cat</td>
      <td>Domestic Short Hair</td>
      <td>NaN</td>
      <td>Domestic Short Hair</td>
      <td>P.O. Box 785</td>
      <td>Newnan</td>
      <td>nchs@nchsrescue.org</td>
      <td>NaN</td>
      <td>GA</td>
      <td>...</td>
      <td>NaN</td>
      <td>M</td>
      <td>GA207</td>
      <td>U2017309</td>
      <td>S</td>
      <td>A</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
  </tbody>
</table>
<p>5 rows × 57 columns</p>
</div>



<a id='pet.get'></a>

### Return a pet record associated with a specific petId

The `pet_get` method can be used to extract a full record from the Petfinder database. We use the pet ID retrieved from the previous call to `pet_getRandom` to illustrate.


```python
pet = pf.pet_get('26417898')
```


```python
pet
```




    {'@encoding': 'iso-8859-1',
     '@version': '1.0',
     'petfinder': {'@xmlns:xsi': 'http://www.w3.org/2001/XMLSchema-instance',
      '@xsi:noNamespaceSchemaLocation': 'http://api.petfinder.com/schemas/0.9/petfinder.xsd',
      'header': {'status': {'code': {'$t': '100'}, 'message': {}},
       'timestamp': {'$t': '2017-11-23T02:45:46Z'},
       'version': {'$t': '0.1'}},
      'pet': {'age': {'$t': 'Young'},
       'animal': {'$t': 'Dog'},
       'breeds': {'breed': {'$t': 'American Staffordshire Terrier'}},
       'contact': {'address1': {'$t': '940 Little Britain Rd.'},
        'address2': {},
        'city': {'$t': 'New Windsor'},
        'email': {'$t': 'info@hudsonvalleyspca.org'},
        'fax': {},
        'phone': {'$t': '845-564-6810 '},
        'state': {'$t': 'NY'},
        'zip': {'$t': '12553'}},
       'description': {'$t': 'Zack is a 5 year old m/n very high energy dog.\xa0 He loves people and is very friendly. Because of his high energy level he needs to be a home with older kids and/or an owner who is an experienced dog owner.'},
       'id': {'$t': '26417898'},
       'lastUpdate': {'$t': '2017-03-09T20:52:21Z'},
       'media': {'photos': {'photo': [{'$t': 'http://photos.petfinder.com/photos/pets/26417898/1/?bust=1371453164&width=60&-pnt.jpg',
           '@id': '1',
           '@size': 'pnt'},
          {'$t': 'http://photos.petfinder.com/photos/pets/26417898/1/?bust=1371453164&width=95&-fpm.jpg',
           '@id': '1',
           '@size': 'fpm'},
          {'$t': 'http://photos.petfinder.com/photos/pets/26417898/1/?bust=1371453164&width=500&-x.jpg',
           '@id': '1',
           '@size': 'x'},
          {'$t': 'http://photos.petfinder.com/photos/pets/26417898/1/?bust=1371453164&width=300&-pn.jpg',
           '@id': '1',
           '@size': 'pn'},
          {'$t': 'http://photos.petfinder.com/photos/pets/26417898/1/?bust=1371453164&width=50&-t.jpg',
           '@id': '1',
           '@size': 't'}]}},
       'mix': {'$t': 'yes'},
       'name': {'$t': 'Zack'},
       'options': {'option': [{'$t': 'hasShots'},
         {'$t': 'noKids'},
         {'$t': 'altered'},
         {'$t': 'noCats'},
         {'$t': 'housetrained'}]},
       'sex': {'$t': 'M'},
       'shelterId': {'$t': 'NY213'},
       'shelterPetId': {},
       'size': {'$t': 'M'},
       'status': {'$t': 'A'}}}}



The record can also be returned as a `DataFrame`.


```python
pf.pet_get('39801731', return_df=True)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>age</th>
      <th>animal</th>
      <th>breeds.breed</th>
      <th>contact.address1</th>
      <th>contact.city</th>
      <th>contact.email</th>
      <th>contact.phone</th>
      <th>contact.state</th>
      <th>contact.zip</th>
      <th>description</th>
      <th>...</th>
      <th>photos20</th>
      <th>photos21</th>
      <th>photos22</th>
      <th>photos23</th>
      <th>photos24</th>
      <th>photos25</th>
      <th>photos26</th>
      <th>photos27</th>
      <th>photos28</th>
      <th>photos29</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Adult</td>
      <td>Cat</td>
      <td>Domestic Medium Hair (Black &amp; White)</td>
      <td>54687 County Road 19</td>
      <td>Bristol</td>
      <td>info@elkharthumanesociety.org</td>
      <td>(574) 848-4225</td>
      <td>IN</td>
      <td>46507</td>
      <td>Please visit our website at www.ElkhartHumaneS...</td>
      <td>...</td>
      <td>http://photos.petfinder.com/photos/pets/398017...</td>
      <td>http://photos.petfinder.com/photos/pets/398017...</td>
      <td>http://photos.petfinder.com/photos/pets/398017...</td>
      <td>http://photos.petfinder.com/photos/pets/398017...</td>
      <td>http://photos.petfinder.com/photos/pets/398017...</td>
      <td>http://photos.petfinder.com/photos/pets/398017...</td>
      <td>http://photos.petfinder.com/photos/pets/398017...</td>
      <td>http://photos.petfinder.com/photos/pets/398017...</td>
      <td>http://photos.petfinder.com/photos/pets/398017...</td>
      <td>http://photos.petfinder.com/photos/pets/398017...</td>
    </tr>
  </tbody>
</table>
<p>1 rows × 54 columns</p>
</div>



The `pets_get()` method accepts a list or tuple and returns the records associated with each pet ID in the passed variable.


```python
petids = random_pet_df['id'].tolist() # get the pet IDs from the previous call by turning the id column into a list
```


```python
pf.pets_get(petids, return_df=True)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>age</th>
      <th>animal</th>
      <th>breed0</th>
      <th>breed1</th>
      <th>breeds.breed</th>
      <th>contact.address1</th>
      <th>contact.city</th>
      <th>contact.email</th>
      <th>contact.phone</th>
      <th>contact.state</th>
      <th>...</th>
      <th>photos9</th>
      <th>sex</th>
      <th>shelterId</th>
      <th>shelterPetId</th>
      <th>size</th>
      <th>status</th>
      <th>status0</th>
      <th>status1</th>
      <th>status2</th>
      <th>status3</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Senior</td>
      <td>Cat</td>
      <td>Domestic Short Hair</td>
      <td>NaN</td>
      <td>Domestic Short Hair</td>
      <td>4081 Columbia Avenue</td>
      <td>Columbia</td>
      <td>catmisonly2@yahoo.com</td>
      <td>717-684-2285</td>
      <td>PA</td>
      <td>...</td>
      <td>NaN</td>
      <td>M</td>
      <td>PA696</td>
      <td>NaN</td>
      <td>S</td>
      <td>A</td>
      <td>hasShots</td>
      <td>altered</td>
      <td>housetrained</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>0</th>
      <td>Adult</td>
      <td>Dog</td>
      <td>Chihuahua</td>
      <td>NaN</td>
      <td>Chihuahua</td>
      <td>NaN</td>
      <td>Romeoville</td>
      <td>info@perfectpooches.org</td>
      <td>NaN</td>
      <td>IL</td>
      <td>...</td>
      <td>http://photos.petfinder.com/photos/pets/397199...</td>
      <td>F</td>
      <td>IL753</td>
      <td>NaN</td>
      <td>S</td>
      <td>A</td>
      <td>hasShots</td>
      <td>altered</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>0</th>
      <td>Adult</td>
      <td>Cat</td>
      <td>Domestic Short Hair (Gray &amp; White)</td>
      <td>NaN</td>
      <td>Domestic Short Hair (Gray &amp; White)</td>
      <td>NaN</td>
      <td>Closter</td>
      <td>clawsadopt@yahoo.com</td>
      <td>(201) 768-0200</td>
      <td>NJ</td>
      <td>...</td>
      <td>http://photos.petfinder.com/photos/pets/386709...</td>
      <td>F</td>
      <td>NJ279</td>
      <td>Marcia</td>
      <td>M</td>
      <td>A</td>
      <td>hasShots</td>
      <td>altered</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>0</th>
      <td>Young</td>
      <td>Dog</td>
      <td>Labrador Retriever</td>
      <td>German Shepherd Dog</td>
      <td>NaN</td>
      <td>PO Box 421</td>
      <td>Ben Wheeler</td>
      <td>admin@vzchumanesociety.org</td>
      <td>903-962-5700</td>
      <td>TX</td>
      <td>...</td>
      <td>http://photos.petfinder.com/photos/pets/317327...</td>
      <td>M</td>
      <td>TX310</td>
      <td>8366590</td>
      <td>L</td>
      <td>A</td>
      <td>specialNeeds</td>
      <td>hasShots</td>
      <td>altered</td>
      <td>housetrained</td>
    </tr>
    <tr>
      <th>0</th>
      <td>Baby</td>
      <td>Cat</td>
      <td>Domestic Short Hair</td>
      <td>NaN</td>
      <td>Domestic Short Hair</td>
      <td>P.O. Box 785</td>
      <td>Newnan</td>
      <td>nchs@nchsrescue.org</td>
      <td>NaN</td>
      <td>GA</td>
      <td>...</td>
      <td>NaN</td>
      <td>M</td>
      <td>GA207</td>
      <td>U2017309</td>
      <td>S</td>
      <td>A</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
  </tbody>
</table>
<p>5 rows × 57 columns</p>
</div>



The `pets_get()` method is essentially a convenience wrapper of `pet_get()`. The same results can be obtained by passing the variable to `pet_get()`.


```python
pf.pet_get(petids, return_df=True)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>age</th>
      <th>animal</th>
      <th>breed0</th>
      <th>breed1</th>
      <th>breeds.breed</th>
      <th>contact.address1</th>
      <th>contact.city</th>
      <th>contact.email</th>
      <th>contact.phone</th>
      <th>contact.state</th>
      <th>...</th>
      <th>photos9</th>
      <th>sex</th>
      <th>shelterId</th>
      <th>shelterPetId</th>
      <th>size</th>
      <th>status</th>
      <th>status0</th>
      <th>status1</th>
      <th>status2</th>
      <th>status3</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Senior</td>
      <td>Cat</td>
      <td>Domestic Short Hair</td>
      <td>NaN</td>
      <td>Domestic Short Hair</td>
      <td>4081 Columbia Avenue</td>
      <td>Columbia</td>
      <td>catmisonly2@yahoo.com</td>
      <td>717-684-2285</td>
      <td>PA</td>
      <td>...</td>
      <td>NaN</td>
      <td>M</td>
      <td>PA696</td>
      <td>NaN</td>
      <td>S</td>
      <td>A</td>
      <td>hasShots</td>
      <td>altered</td>
      <td>housetrained</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>0</th>
      <td>Adult</td>
      <td>Dog</td>
      <td>Chihuahua</td>
      <td>NaN</td>
      <td>Chihuahua</td>
      <td>NaN</td>
      <td>Romeoville</td>
      <td>info@perfectpooches.org</td>
      <td>NaN</td>
      <td>IL</td>
      <td>...</td>
      <td>http://photos.petfinder.com/photos/pets/397199...</td>
      <td>F</td>
      <td>IL753</td>
      <td>NaN</td>
      <td>S</td>
      <td>A</td>
      <td>hasShots</td>
      <td>altered</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>0</th>
      <td>Adult</td>
      <td>Cat</td>
      <td>Domestic Short Hair (Gray &amp; White)</td>
      <td>NaN</td>
      <td>Domestic Short Hair (Gray &amp; White)</td>
      <td>NaN</td>
      <td>Closter</td>
      <td>clawsadopt@yahoo.com</td>
      <td>(201) 768-0200</td>
      <td>NJ</td>
      <td>...</td>
      <td>http://photos.petfinder.com/photos/pets/386709...</td>
      <td>F</td>
      <td>NJ279</td>
      <td>Marcia</td>
      <td>M</td>
      <td>A</td>
      <td>hasShots</td>
      <td>altered</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>0</th>
      <td>Young</td>
      <td>Dog</td>
      <td>Labrador Retriever</td>
      <td>German Shepherd Dog</td>
      <td>NaN</td>
      <td>PO Box 421</td>
      <td>Ben Wheeler</td>
      <td>admin@vzchumanesociety.org</td>
      <td>903-962-5700</td>
      <td>TX</td>
      <td>...</td>
      <td>http://photos.petfinder.com/photos/pets/317327...</td>
      <td>M</td>
      <td>TX310</td>
      <td>8366590</td>
      <td>L</td>
      <td>A</td>
      <td>specialNeeds</td>
      <td>hasShots</td>
      <td>altered</td>
      <td>housetrained</td>
    </tr>
    <tr>
      <th>0</th>
      <td>Baby</td>
      <td>Cat</td>
      <td>Domestic Short Hair</td>
      <td>NaN</td>
      <td>Domestic Short Hair</td>
      <td>P.O. Box 785</td>
      <td>Newnan</td>
      <td>nchs@nchsrescue.org</td>
      <td>NaN</td>
      <td>GA</td>
      <td>...</td>
      <td>NaN</td>
      <td>M</td>
      <td>GA207</td>
      <td>U2017309</td>
      <td>S</td>
      <td>A</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
  </tbody>
</table>
<p>5 rows × 57 columns</p>
</div>



<a id='pet.find'></a>

### Finding pet records matching particular search criteria

The `pet.find()` method returns a collection of pet records that match the input search criteria. The available search criteria are listed in the [petpy API documentation](http://petpy.readthedocs.io/en/latest/api.html#pet-methods).

For example, let's say we are interested in finding female cats in Washington state and we want the results returned in a tidy pandas DataFrame.


```python
cats = pf.pet_find(location='WA', animal='cat', sex='F', return_df=True)
```


```python
cats.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>age</th>
      <th>animal</th>
      <th>contact.address1</th>
      <th>contact.city</th>
      <th>contact.email</th>
      <th>contact.phone</th>
      <th>contact.state</th>
      <th>contact.zip</th>
      <th>description</th>
      <th>id</th>
      <th>...</th>
      <th>photos15</th>
      <th>photos16</th>
      <th>photos17</th>
      <th>photos18</th>
      <th>photos19</th>
      <th>photos20</th>
      <th>photos21</th>
      <th>photos22</th>
      <th>photos23</th>
      <th>photos24</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Young</td>
      <td>Cat</td>
      <td>NaN</td>
      <td>Auburn</td>
      <td>pugetsoundrescue@hotmail.com</td>
      <td>NaN</td>
      <td>WA</td>
      <td>98092</td>
      <td>NaN</td>
      <td>39898075</td>
      <td>...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>0</th>
      <td>Adult</td>
      <td>Cat</td>
      <td>21615 64th Ave S</td>
      <td>Kent</td>
      <td>adoptapet@kingcounty.gov</td>
      <td>206-296-7387</td>
      <td>WA</td>
      <td>98032</td>
      <td>This is my friend Gertie. She is a 10-year-old...</td>
      <td>37949653</td>
      <td>...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>0</th>
      <td>Senior</td>
      <td>Cat</td>
      <td>21615 64th Ave S</td>
      <td>Kent</td>
      <td>adoptapet@kingcounty.gov</td>
      <td>206-296-7387</td>
      <td>WA</td>
      <td>98032</td>
      <td>Boo Kitty / Blue Kitty (is that a Russian Blue...</td>
      <td>39921493</td>
      <td>...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>0</th>
      <td>Senior</td>
      <td>Cat</td>
      <td>8103 161st Ave NE</td>
      <td>Redmond</td>
      <td>info@thewhole-cat.com</td>
      <td>425-576-5548</td>
      <td>WA</td>
      <td>98052</td>
      <td>Our adoptions program is a relay for 2-6 partn...</td>
      <td>38792526</td>
      <td>...</td>
      <td>http://photos.petfinder.com/photos/pets/387925...</td>
      <td>http://photos.petfinder.com/photos/pets/387925...</td>
      <td>http://photos.petfinder.com/photos/pets/387925...</td>
      <td>http://photos.petfinder.com/photos/pets/387925...</td>
      <td>http://photos.petfinder.com/photos/pets/387925...</td>
      <td>http://photos.petfinder.com/photos/pets/387925...</td>
      <td>http://photos.petfinder.com/photos/pets/387925...</td>
      <td>http://photos.petfinder.com/photos/pets/387925...</td>
      <td>http://photos.petfinder.com/photos/pets/387925...</td>
      <td>http://photos.petfinder.com/photos/pets/387925...</td>
    </tr>
    <tr>
      <th>0</th>
      <td>Adult</td>
      <td>Cat</td>
      <td>8103 161st Ave NE</td>
      <td>Redmond</td>
      <td>info@thewhole-cat.com</td>
      <td>425-576-5548</td>
      <td>WA</td>
      <td>98052</td>
      <td>Our adoptions program is a relay for 2-6 partn...</td>
      <td>38843221</td>
      <td>...</td>
      <td>http://photos.petfinder.com/photos/pets/388432...</td>
      <td>http://photos.petfinder.com/photos/pets/388432...</td>
      <td>http://photos.petfinder.com/photos/pets/388432...</td>
      <td>http://photos.petfinder.com/photos/pets/388432...</td>
      <td>http://photos.petfinder.com/photos/pets/388432...</td>
      <td>http://photos.petfinder.com/photos/pets/388432...</td>
      <td>http://photos.petfinder.com/photos/pets/388432...</td>
      <td>http://photos.petfinder.com/photos/pets/388432...</td>
      <td>http://photos.petfinder.com/photos/pets/388432...</td>
      <td>http://photos.petfinder.com/photos/pets/388432...</td>
    </tr>
  </tbody>
</table>
<p>5 rows × 55 columns</p>
</div>



The default amount of records returned is 25, which can be changed by setting the `count` parameter. For large queries, it is recommended to set the `pages` parameter with a smaller `count` value. For example, if we wanted to return 1000 results, we could set the `pages` parameter to 10 and the `count` parameter to 100. Please note the Petfinder API places a hard cap of 2,000 results returned per query.

<a id='sheltermethods'></a>

## Shelter Methods

Shelter methods are quite similar to the pet methods explored previously but return information on the animal welfare organizations available in Petfinder's database.

<a id='shelter.find'></a>

### Finding animal welfare organizations in a certain area

The `shelter_find()` method can be used to return shelter records matching the input search criteria. Let's say we want to find 10 shelters listed in the Petfinder database located in Washington State as a pandas DataFrame.


```python
wa_shelters = pf.shelter_find(location='WA', count=10, return_df=True)
```


```python
wa_shelters
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>address1</th>
      <th>address2</th>
      <th>city</th>
      <th>country</th>
      <th>email</th>
      <th>id</th>
      <th>latitude</th>
      <th>longitude</th>
      <th>name</th>
      <th>phone</th>
      <th>state</th>
      <th>zip</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>NaN</td>
      <td>NaN</td>
      <td>Auburn</td>
      <td>US</td>
      <td>pugetsoundrescue@hotmail.com</td>
      <td>WA149</td>
      <td>47.3191</td>
      <td>-122.2682</td>
      <td>Puget Sound Rescue</td>
      <td>NaN</td>
      <td>WA</td>
      <td>98092</td>
    </tr>
    <tr>
      <th>1</th>
      <td>NaN</td>
      <td>NaN</td>
      <td>Auburn</td>
      <td>US</td>
      <td>foggycreekcavyrescue@yahoo.com</td>
      <td>WA254</td>
      <td>47.3191</td>
      <td>-122.2682</td>
      <td>Foggy Creek Cavy Rescue</td>
      <td>NaN</td>
      <td>WA</td>
      <td>98092</td>
    </tr>
    <tr>
      <th>2</th>
      <td>21615 64th Ave S</td>
      <td>NaN</td>
      <td>Kent</td>
      <td>US</td>
      <td>adoptapet@kingcounty.gov</td>
      <td>WA252</td>
      <td>47.3747</td>
      <td>-122.2775</td>
      <td>Regional Animal Services of King County - Fost...</td>
      <td>206-296-7387</td>
      <td>WA</td>
      <td>98032</td>
    </tr>
    <tr>
      <th>3</th>
      <td>21615 64th Ave S.</td>
      <td>NaN</td>
      <td>Kent</td>
      <td>US</td>
      <td>adoptapet@kingcounty.gov</td>
      <td>WA63</td>
      <td>47.3747</td>
      <td>-122.2775</td>
      <td>Regional Animal Services of King County</td>
      <td>206-296-3936</td>
      <td>WA</td>
      <td>98032</td>
    </tr>
    <tr>
      <th>4</th>
      <td>NaN</td>
      <td>NaN</td>
      <td>Redmond</td>
      <td>US</td>
      <td>pacosrescue@yahoo.com</td>
      <td>WA604</td>
      <td>47.3311</td>
      <td>-122.3592</td>
      <td>Pacos Rescue Network</td>
      <td>NaN</td>
      <td>WA</td>
      <td>98052</td>
    </tr>
    <tr>
      <th>5</th>
      <td>PO Box 13244</td>
      <td>NaN</td>
      <td>Des Moines</td>
      <td>US</td>
      <td>anotherchancecats2007@gmail.com</td>
      <td>WA401</td>
      <td>47.4043</td>
      <td>-122.3105</td>
      <td>Another Chance Cat Adoption</td>
      <td>(253) 856-1771</td>
      <td>WA</td>
      <td>98198</td>
    </tr>
    <tr>
      <th>6</th>
      <td>20613 SE 291ST PL</td>
      <td>NaN</td>
      <td>Kent</td>
      <td>US</td>
      <td>PSWC_Adoption@hotmail.com</td>
      <td>WA416</td>
      <td>47.3718</td>
      <td>-122.1474</td>
      <td>Puget Sound Working Cats</td>
      <td>(206) 819-4261</td>
      <td>WA</td>
      <td>98042</td>
    </tr>
    <tr>
      <th>7</th>
      <td>16915 SE 272nd St.</td>
      <td>#100-210</td>
      <td>Covington</td>
      <td>US</td>
      <td>smidgetrescue@hotmail.com</td>
      <td>WA544</td>
      <td>47.3718</td>
      <td>-122.1474</td>
      <td>Smidget Rescue</td>
      <td>206.817.3731</td>
      <td>WA</td>
      <td>98042</td>
    </tr>
    <tr>
      <th>8</th>
      <td>NaN</td>
      <td>NaN</td>
      <td>Covington</td>
      <td>US</td>
      <td>adoptions.leftbehindk9@gmail.com</td>
      <td>WA555</td>
      <td>47.3718</td>
      <td>-122.1474</td>
      <td>Left Behind K-9 Rescue</td>
      <td>NaN</td>
      <td>WA</td>
      <td>98042</td>
    </tr>
    <tr>
      <th>9</th>
      <td>1102 E. Main Ave</td>
      <td>NaN</td>
      <td>Puyallup</td>
      <td>US</td>
      <td>info@sunnyskysshelter.org</td>
      <td>WA470</td>
      <td>47.2032</td>
      <td>-122.2738</td>
      <td>Sunny Sky's Animal Rescue</td>
      <td>NaN</td>
      <td>WA</td>
      <td>98372</td>
    </tr>
  </tbody>
</table>
</div>



<a id='shelter.get'></a>

### Returning specific shelter information

The `shelter_get()` method returns the available information in the Petfinder database matching the given shelter ID. Shelter IDs can be found using the `shelter_find()` method used earlier. For example, let's use the method to return the record matching the first shelter ID in the result set obtained in the previous example.


```python
shelter_list = wa_shelters['id'].tolist()
```


```python
pf.shelter_get(shelter_list[0])
```




    {'@encoding': 'iso-8859-1',
     '@version': '1.0',
     'petfinder': {'@xmlns:xsi': 'http://www.w3.org/2001/XMLSchema-instance',
      '@xsi:noNamespaceSchemaLocation': 'http://api.petfinder.com/schemas/0.9/petfinder.xsd',
      'header': {'status': {'code': {'$t': '100'}, 'message': {}},
       'timestamp': {'$t': '2017-11-23T02:46:10Z'},
       'version': {'$t': '0.1'}},
      'shelter': {'address1': {},
       'address2': {},
       'city': {'$t': 'Auburn'},
       'country': {'$t': 'US'},
       'email': {'$t': 'pugetsoundrescue@hotmail.com'},
       'fax': {},
       'id': {'$t': 'WA149'},
       'latitude': {'$t': '47.3191'},
       'longitude': {'$t': '-122.2682'},
       'name': {'$t': 'Puget Sound Rescue'},
       'phone': {},
       'state': {'$t': 'WA'},
       'zip': {'$t': '98092'}}}}



The `shelter_get()` method can also accept a list or tuple of shelter IDs. Internally, this calls a convenience wrapper method `shelters_get()`.


```python
pf.shelters_get(shelter_list, return_df=True)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>address1</th>
      <th>address2</th>
      <th>city</th>
      <th>country</th>
      <th>email</th>
      <th>id</th>
      <th>latitude</th>
      <th>longitude</th>
      <th>name</th>
      <th>phone</th>
      <th>state</th>
      <th>zip</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>NaN</td>
      <td>NaN</td>
      <td>Auburn</td>
      <td>US</td>
      <td>pugetsoundrescue@hotmail.com</td>
      <td>WA149</td>
      <td>47.3191</td>
      <td>-122.2682</td>
      <td>Puget Sound Rescue</td>
      <td>NaN</td>
      <td>WA</td>
      <td>98092</td>
    </tr>
    <tr>
      <th>0</th>
      <td>NaN</td>
      <td>NaN</td>
      <td>Auburn</td>
      <td>US</td>
      <td>foggycreekcavyrescue@yahoo.com</td>
      <td>WA254</td>
      <td>47.3191</td>
      <td>-122.2682</td>
      <td>Foggy Creek Cavy Rescue</td>
      <td>NaN</td>
      <td>WA</td>
      <td>98092</td>
    </tr>
    <tr>
      <th>0</th>
      <td>21615 64th Ave S</td>
      <td>NaN</td>
      <td>Kent</td>
      <td>US</td>
      <td>adoptapet@kingcounty.gov</td>
      <td>WA252</td>
      <td>47.3747</td>
      <td>-122.2775</td>
      <td>Regional Animal Services of King County - Fost...</td>
      <td>206-296-7387</td>
      <td>WA</td>
      <td>98032</td>
    </tr>
    <tr>
      <th>0</th>
      <td>21615 64th Ave S.</td>
      <td>NaN</td>
      <td>Kent</td>
      <td>US</td>
      <td>adoptapet@kingcounty.gov</td>
      <td>WA63</td>
      <td>47.3747</td>
      <td>-122.2775</td>
      <td>Regional Animal Services of King County</td>
      <td>206-296-3936</td>
      <td>WA</td>
      <td>98032</td>
    </tr>
    <tr>
      <th>0</th>
      <td>NaN</td>
      <td>NaN</td>
      <td>Redmond</td>
      <td>US</td>
      <td>pacosrescue@yahoo.com</td>
      <td>WA604</td>
      <td>47.3311</td>
      <td>-122.3592</td>
      <td>Pacos Rescue Network</td>
      <td>NaN</td>
      <td>WA</td>
      <td>98052</td>
    </tr>
    <tr>
      <th>0</th>
      <td>PO Box 13244</td>
      <td>NaN</td>
      <td>Des Moines</td>
      <td>US</td>
      <td>anotherchancecats2007@gmail.com</td>
      <td>WA401</td>
      <td>47.4043</td>
      <td>-122.3105</td>
      <td>Another Chance Cat Adoption</td>
      <td>(253) 856-1771</td>
      <td>WA</td>
      <td>98198</td>
    </tr>
    <tr>
      <th>0</th>
      <td>20613 SE 291ST PL</td>
      <td>NaN</td>
      <td>Kent</td>
      <td>US</td>
      <td>PSWC_Adoption@hotmail.com</td>
      <td>WA416</td>
      <td>47.3718</td>
      <td>-122.1474</td>
      <td>Puget Sound Working Cats</td>
      <td>(206) 819-4261</td>
      <td>WA</td>
      <td>98042</td>
    </tr>
    <tr>
      <th>0</th>
      <td>16915 SE 272nd St.</td>
      <td>#100-210</td>
      <td>Covington</td>
      <td>US</td>
      <td>smidgetrescue@hotmail.com</td>
      <td>WA544</td>
      <td>47.3718</td>
      <td>-122.1474</td>
      <td>Smidget Rescue</td>
      <td>206.817.3731</td>
      <td>WA</td>
      <td>98042</td>
    </tr>
    <tr>
      <th>0</th>
      <td>NaN</td>
      <td>NaN</td>
      <td>Covington</td>
      <td>US</td>
      <td>adoptions.leftbehindk9@gmail.com</td>
      <td>WA555</td>
      <td>47.3718</td>
      <td>-122.1474</td>
      <td>Left Behind K-9 Rescue</td>
      <td>NaN</td>
      <td>WA</td>
      <td>98042</td>
    </tr>
    <tr>
      <th>0</th>
      <td>1102 E. Main Ave</td>
      <td>NaN</td>
      <td>Puyallup</td>
      <td>US</td>
      <td>info@sunnyskysshelter.org</td>
      <td>WA470</td>
      <td>47.2032</td>
      <td>-122.2738</td>
      <td>Sunny Sky's Animal Rescue</td>
      <td>NaN</td>
      <td>WA</td>
      <td>98372</td>
    </tr>
  </tbody>
</table>
</div>



The result obtained would be the same if one were to use the `shelter_get()` method and passed the same variable.

<a id='shelter.getPets'></a>

### Extracting pet records from a particular shelter

The `shelter.getPets()` method returns the pet records that belong to a particular shelter ID. For example, let's say we want to return the pet records from the first shelter in our list as a DataFrame.


```python
shelter_pets = pf.shelter_getPets(shelter_list[0], return_df=True)
shelter_pets.head() # The default number of returned records is 25, so we only print the first 5 rows for brevity
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>age</th>
      <th>animal</th>
      <th>contact.city</th>
      <th>contact.email</th>
      <th>contact.state</th>
      <th>contact.zip</th>
      <th>description</th>
      <th>id</th>
      <th>lastUpdate</th>
      <th>media.photos.photo</th>
      <th>...</th>
      <th>photos15</th>
      <th>photos16</th>
      <th>photos17</th>
      <th>photos18</th>
      <th>photos19</th>
      <th>photos20</th>
      <th>photos21</th>
      <th>photos22</th>
      <th>photos23</th>
      <th>photos24</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Adult</td>
      <td>Dog</td>
      <td>Auburn</td>
      <td>pugetsoundrescue@hotmail.com</td>
      <td>WA</td>
      <td>98092</td>
      <td>Morena is a shepherd/lab mix we are guessing, ...</td>
      <td>32080691</td>
      <td>2017-09-01T23:26:37Z</td>
      <td>[{'@size': 'pnt', '$t': 'http://photos.petfind...</td>
      <td>...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>0</th>
      <td>Adult</td>
      <td>Dog</td>
      <td>Auburn</td>
      <td>pugetsoundrescue@hotmail.com</td>
      <td>WA</td>
      <td>98092</td>
      <td>Monty is a loving gentleman that likes long wa...</td>
      <td>34906970</td>
      <td>2017-09-01T23:26:59Z</td>
      <td>[{'@size': 'pnt', '$t': 'http://photos.petfind...</td>
      <td>...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>0</th>
      <td>Adult</td>
      <td>Dog</td>
      <td>Auburn</td>
      <td>pugetsoundrescue@hotmail.com</td>
      <td>WA</td>
      <td>98092</td>
      <td>ADOPTION DONATION: $350\n\nCONTACT US TODAY: P...</td>
      <td>37760609</td>
      <td>2017-11-01T05:01:56Z</td>
      <td>[{'@size': 'pnt', '$t': 'http://photos.petfind...</td>
      <td>...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>0</th>
      <td>Young</td>
      <td>Dog</td>
      <td>Auburn</td>
      <td>pugetsoundrescue@hotmail.com</td>
      <td>WA</td>
      <td>98092</td>
      <td>ADOPTION DONATION: $350\n\nCONTACT US TODAY: P...</td>
      <td>38602092</td>
      <td>2017-09-01T21:00:13Z</td>
      <td>[{'@size': 'pnt', '$t': 'http://photos.petfind...</td>
      <td>...</td>
      <td>http://photos.petfinder.com/photos/pets/386020...</td>
      <td>http://photos.petfinder.com/photos/pets/386020...</td>
      <td>http://photos.petfinder.com/photos/pets/386020...</td>
      <td>http://photos.petfinder.com/photos/pets/386020...</td>
      <td>http://photos.petfinder.com/photos/pets/386020...</td>
      <td>http://photos.petfinder.com/photos/pets/386020...</td>
      <td>http://photos.petfinder.com/photos/pets/386020...</td>
      <td>http://photos.petfinder.com/photos/pets/386020...</td>
      <td>http://photos.petfinder.com/photos/pets/386020...</td>
      <td>http://photos.petfinder.com/photos/pets/386020...</td>
    </tr>
    <tr>
      <th>0</th>
      <td>Adult</td>
      <td>Dog</td>
      <td>Auburn</td>
      <td>pugetsoundrescue@hotmail.com</td>
      <td>WA</td>
      <td>98092</td>
      <td>ADOPTION DONATION: $350\n\nCONTACT US TODAY: P...</td>
      <td>38627371</td>
      <td>2017-11-20T13:54:50Z</td>
      <td>[{'@size': 'pnt', '$t': 'http://photos.petfind...</td>
      <td>...</td>
      <td>http://photos.petfinder.com/photos/pets/386273...</td>
      <td>http://photos.petfinder.com/photos/pets/386273...</td>
      <td>http://photos.petfinder.com/photos/pets/386273...</td>
      <td>http://photos.petfinder.com/photos/pets/386273...</td>
      <td>http://photos.petfinder.com/photos/pets/386273...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
  </tbody>
</table>
<p>5 rows × 48 columns</p>
</div>



<a id='shelter.listByBreed'></a>

### Finding shelters that have records matching a particular animal breed

The `shelter_listByBreeds()` method allows the user to find shelters that match pet records of a the input animal breed. This method is best used in conjunction with the `breed_list()` method to find the available animal breeds in the Petfinder database.

We already extracted the available cat breeds earlier in the introduction, which we can use to select a cat breed listed in the Petfinder database.


```python
cats_df.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>cat breeds</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Abyssinian</td>
    </tr>
    <tr>
      <th>1</th>
      <td>American Curl</td>
    </tr>
    <tr>
      <th>2</th>
      <td>American Shorthair</td>
    </tr>
    <tr>
      <th>3</th>
      <td>American Wirehair</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Applehead Siamese</td>
    </tr>
  </tbody>
</table>
</div>



The Abyssinian is a beautiful breed of cat, let's find some shelters that have pet records matching an Abyssinian breed and return it as a DataFrame.


```python
aby = cats_df['cat breeds'].tolist()[0]
```


```python
aby_shelters = pf.shelter_listByBreed('cat', aby, return_df=True)
aby_shelters.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>address1</th>
      <th>address2</th>
      <th>city</th>
      <th>country</th>
      <th>email</th>
      <th>id</th>
      <th>latitude</th>
      <th>longitude</th>
      <th>name</th>
      <th>phone</th>
      <th>state</th>
      <th>zip</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>5473 Overpass Road</td>
      <td>NaN</td>
      <td>Santa Barbara</td>
      <td>US</td>
      <td>SBAdoption@sbcphd.org</td>
      <td>CA63</td>
      <td>34.4427</td>
      <td>-119.8024</td>
      <td>Santa Barbara County Animal Services--Santa Ba...</td>
      <td>805-681-5285</td>
      <td>CA</td>
      <td>93111</td>
    </tr>
    <tr>
      <th>1</th>
      <td>P. O. Box 6356</td>
      <td>NaN</td>
      <td>Brandon</td>
      <td>US</td>
      <td>CatcallFL@gmail.com</td>
      <td>FL472</td>
      <td>27.909</td>
      <td>-82.2845</td>
      <td>Cat Call Inc.</td>
      <td>(813) 324-9320</td>
      <td>FL</td>
      <td>33511</td>
    </tr>
    <tr>
      <th>2</th>
      <td>1447 Folly Road</td>
      <td>NaN</td>
      <td>Charleston</td>
      <td>US</td>
      <td>adoption@pethelpers.org</td>
      <td>SC120</td>
      <td>32.7357</td>
      <td>-79.9553</td>
      <td>Pet Helpers Inc.</td>
      <td>843.795.1110</td>
      <td>SC</td>
      <td>29412</td>
    </tr>
    <tr>
      <th>3</th>
      <td>6111 Highland Drive</td>
      <td>NaN</td>
      <td>Jonesboro</td>
      <td>US</td>
      <td>margaret@neahs.org</td>
      <td>AR128</td>
      <td>35.8213</td>
      <td>-90.6996</td>
      <td>NEA Humane Society</td>
      <td>(870) 932/5185</td>
      <td>AR</td>
      <td>72401</td>
    </tr>
    <tr>
      <th>4</th>
      <td>P.O. Box  1521</td>
      <td>NaN</td>
      <td>Malvern</td>
      <td>US</td>
      <td>mataft@netscape.com</td>
      <td>AR238</td>
      <td>34.1569</td>
      <td>-92.9206</td>
      <td>Stop Animal Cruelty in Hot Spring County</td>
      <td>(501) 276-2385</td>
      <td>AR</td>
      <td>72104</td>
    </tr>
  </tbody>
</table>
</div>


