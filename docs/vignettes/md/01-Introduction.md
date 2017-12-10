
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
       'timestamp': {'$t': '2017-11-22T16:57:26Z'},
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
       'timestamp': {'$t': '2017-11-21T19:06:51Z'},
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
       'timestamp': {'$t': '2017-11-21T19:06:54Z'},
       'version': {'$t': '0.1'}},
      'petIds': {'id': {'$t': '39801731'}}}}



The default record output contains only the pet record's ID and the call's JSON metadata. If we wish to return a more complete random pet record, we can set the parameter `output` to `basic` (name, age, animal, breed, shelterID) or `full` (complete record with description).


```python
pf.pet_getRandom(output='full')
```




    {'@encoding': 'iso-8859-1',
     '@version': '1.0',
     'petfinder': {'@xmlns:xsi': 'http://www.w3.org/2001/XMLSchema-instance',
      '@xsi:noNamespaceSchemaLocation': 'http://api.petfinder.com/schemas/0.9/petfinder.xsd',
      'header': {'status': {'code': {'$t': '100'}, 'message': {}},
       'timestamp': {'$t': '2017-11-21T19:06:58Z'},
       'version': {'$t': '0.1'}},
      'pet': {'age': {'$t': 'Adult'},
       'animal': {'$t': 'Dog'},
       'breeds': {'breed': {'$t': 'Chihuahua'}},
       'contact': {'address1': {},
        'address2': {},
        'city': {'$t': 'Parkland'},
        'email': {'$t': 'info@getalifepetrescue.com'},
        'fax': {},
        'phone': {'$t': '954-629-2445'},
        'state': {'$t': 'FL'},
        'zip': {'$t': '33067'}},
       'description': {'$t': "Shakira Long Haired Chihuahua is approximately 6-7-year-old, 6.5-pound bundle of joy. She so very much wants to be loved and she shows it with her head tilts as she tunes into your baby talk while she wags her tail. She is a sweet girl who arrived at us as a stray so the vet is figuring her age by her blood work, teeth, and her eyes. She is healthy and she has received a dental cleaning along with her other vetting. She enjoys being next to you and is good with other dogs so she would make a great addition to your doggy home. SHe is a wonderful companion. She is calm and sweet so she is the perfect package. \nHer adoption fee is $300 to go towards her vetting (vaccines, spay/neuter, heartworm/Ehrlichia/Lyme test, fecal test, pre-op blood work, dental cleaning, and microchip). If you are interested in adopting please fill out the adoption application} http://www.getalifepetrescue.com/galpr-info/adoption-application.html\n\nAdoption Procedure:\nFill out our Adoption Application\nMeet with the dog(s)Home check\nAdoption Contract\nAdoption Donation (Between $150-$400)\n\nMedical Care That We Give To Our Rescued Pets:\nComplete Physical Examination\nSpay or Neuter Surgery\nHeartworm/Ehrlichia/Lyme Tested\nFecal Exam\nVACCINES~ Bordatella, Distemper, Rabies, Parvo, Corona, Adenovirus Type-2  \nDewormed\nMicrochipped plus lifetime registration (not for cats)\nGrooming (as needed)\nDental Cleaning (if needed)\nStarted on Heartworm Preventative and Flea & Tick Preventative\n\nWhat Makes A Qualified Adopter:\nApplicant must be 21 years or older Applicant's current pet should be up-to-date with appropriate vaccines Applicant's current pet must be altered, unless medical reasons do not permit All people in household need be present for home check Need Landlord or Home Owners Association's approval (if applicable) to have a pet  Applicant must be in the state of Florida preferable in Dade, Broward or Palm Beach Counties."},
       'id': {'$t': '39881634'},
       'lastUpdate': {'$t': '2017-11-10T19:17:04Z'},
       'media': {'photos': {'photo': [{'$t': 'http://photos.petfinder.com/photos/pets/39881634/1/?bust=1510340490&width=60&-pnt.jpg',
           '@id': '1',
           '@size': 'pnt'},
          {'$t': 'http://photos.petfinder.com/photos/pets/39881634/1/?bust=1510340490&width=95&-fpm.jpg',
           '@id': '1',
           '@size': 'fpm'},
          {'$t': 'http://photos.petfinder.com/photos/pets/39881634/1/?bust=1510340490&width=500&-x.jpg',
           '@id': '1',
           '@size': 'x'},
          {'$t': 'http://photos.petfinder.com/photos/pets/39881634/1/?bust=1510340490&width=300&-pn.jpg',
           '@id': '1',
           '@size': 'pn'},
          {'$t': 'http://photos.petfinder.com/photos/pets/39881634/1/?bust=1510340490&width=50&-t.jpg',
           '@id': '1',
           '@size': 't'},
          {'$t': 'http://photos.petfinder.com/photos/pets/39881634/2/?bust=1510340495&width=60&-pnt.jpg',
           '@id': '2',
           '@size': 'pnt'},
          {'$t': 'http://photos.petfinder.com/photos/pets/39881634/2/?bust=1510340495&width=95&-fpm.jpg',
           '@id': '2',
           '@size': 'fpm'},
          {'$t': 'http://photos.petfinder.com/photos/pets/39881634/2/?bust=1510340495&width=500&-x.jpg',
           '@id': '2',
           '@size': 'x'},
          {'$t': 'http://photos.petfinder.com/photos/pets/39881634/2/?bust=1510340495&width=300&-pn.jpg',
           '@id': '2',
           '@size': 'pn'},
          {'$t': 'http://photos.petfinder.com/photos/pets/39881634/2/?bust=1510340495&width=50&-t.jpg',
           '@id': '2',
           '@size': 't'},
          {'$t': 'http://photos.petfinder.com/photos/pets/39881634/3/?bust=1510340500&width=60&-pnt.jpg',
           '@id': '3',
           '@size': 'pnt'},
          {'$t': 'http://photos.petfinder.com/photos/pets/39881634/3/?bust=1510340500&width=95&-fpm.jpg',
           '@id': '3',
           '@size': 'fpm'},
          {'$t': 'http://photos.petfinder.com/photos/pets/39881634/3/?bust=1510340500&width=500&-x.jpg',
           '@id': '3',
           '@size': 'x'},
          {'$t': 'http://photos.petfinder.com/photos/pets/39881634/3/?bust=1510340500&width=300&-pn.jpg',
           '@id': '3',
           '@size': 'pn'},
          {'$t': 'http://photos.petfinder.com/photos/pets/39881634/3/?bust=1510340500&width=50&-t.jpg',
           '@id': '3',
           '@size': 't'},
          {'$t': 'http://photos.petfinder.com/photos/pets/39881634/4/?bust=1510340515&width=60&-pnt.jpg',
           '@id': '4',
           '@size': 'pnt'},
          {'$t': 'http://photos.petfinder.com/photos/pets/39881634/4/?bust=1510340515&width=95&-fpm.jpg',
           '@id': '4',
           '@size': 'fpm'},
          {'$t': 'http://photos.petfinder.com/photos/pets/39881634/4/?bust=1510340515&width=500&-x.jpg',
           '@id': '4',
           '@size': 'x'},
          {'$t': 'http://photos.petfinder.com/photos/pets/39881634/4/?bust=1510340515&width=300&-pn.jpg',
           '@id': '4',
           '@size': 'pn'},
          {'$t': 'http://photos.petfinder.com/photos/pets/39881634/4/?bust=1510340515&width=50&-t.jpg',
           '@id': '4',
           '@size': 't'},
          {'$t': 'http://photos.petfinder.com/photos/pets/39881634/5/?bust=1510340519&width=60&-pnt.jpg',
           '@id': '5',
           '@size': 'pnt'},
          {'$t': 'http://photos.petfinder.com/photos/pets/39881634/5/?bust=1510340519&width=95&-fpm.jpg',
           '@id': '5',
           '@size': 'fpm'},
          {'$t': 'http://photos.petfinder.com/photos/pets/39881634/5/?bust=1510340519&width=500&-x.jpg',
           '@id': '5',
           '@size': 'x'},
          {'$t': 'http://photos.petfinder.com/photos/pets/39881634/5/?bust=1510340519&width=300&-pn.jpg',
           '@id': '5',
           '@size': 'pn'},
          {'$t': 'http://photos.petfinder.com/photos/pets/39881634/5/?bust=1510340519&width=50&-t.jpg',
           '@id': '5',
           '@size': 't'}]}},
       'mix': {'$t': 'no'},
       'name': {'$t': 'Shakira'},
       'options': {'option': [{'$t': 'hasShots'},
         {'$t': 'altered'},
         {'$t': 'housetrained'}]},
       'sex': {'$t': 'F'},
       'shelterId': {'$t': 'FL597'},
       'shelterPetId': {'$t': 'shakira'},
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
      <td>Adult</td>
      <td>Dog</td>
      <td>Boxer</td>
      <td>Labrador Retriever</td>
      <td>NaN</td>
      <td>PO Box 60935</td>
      <td>Fort Myers</td>
      <td>rescueanimalsinneed@gmail.com</td>
      <td>407-414-2866</td>
      <td>FL</td>
      <td>...</td>
      <td>http://photos.petfinder.com/photos/pets/367743...</td>
      <td>F</td>
      <td>FL1027</td>
      <td>NaN</td>
      <td>M</td>
      <td>A</td>
      <td>hasShots</td>
      <td>noKids</td>
      <td>altered</td>
      <td>housetrained</td>
    </tr>
    <tr>
      <th>0</th>
      <td>Young</td>
      <td>Dog</td>
      <td>Beagle</td>
      <td>NaN</td>
      <td>Beagle</td>
      <td>P.O. Box 402</td>
      <td>Liberty Center</td>
      <td>heritagefarms08@gmail.com</td>
      <td>419-591-6621</td>
      <td>OH</td>
      <td>...</td>
      <td>http://photos.petfinder.com/photos/pets/391432...</td>
      <td>M</td>
      <td>OH743</td>
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
      <td>Domestic Short Hair</td>
      <td>NaN</td>
      <td>Domestic Short Hair</td>
      <td>NaN</td>
      <td>Kansas City</td>
      <td>coquina2@aol.com</td>
      <td>NaN</td>
      <td>MO</td>
      <td>...</td>
      <td>http://photos.petfinder.com/photos/pets/314172...</td>
      <td>M</td>
      <td>MO608</td>
      <td>NaN</td>
      <td>M</td>
      <td>A</td>
      <td>hasShots</td>
      <td>noDogs</td>
      <td>altered</td>
      <td>housetrained</td>
    </tr>
    <tr>
      <th>0</th>
      <td>Adult</td>
      <td>Cat</td>
      <td>Domestic Short Hair</td>
      <td>NaN</td>
      <td>Domestic Short Hair</td>
      <td>185 N Industrial Drive</td>
      <td>Erwin</td>
      <td>unicoicountyanimalshelter@gmail.com</td>
      <td>423-743-3071</td>
      <td>TN</td>
      <td>...</td>
      <td>http://photos.petfinder.com/photos/pets/394589...</td>
      <td>F</td>
      <td>TN489</td>
      <td>12046973</td>
      <td>M</td>
      <td>A</td>
      <td>altered</td>
      <td>housetrained</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>0</th>
      <td>Young</td>
      <td>Dog</td>
      <td>Rottweiler</td>
      <td>NaN</td>
      <td>Rottweiler</td>
      <td>3550 Aumsville Hwy SE</td>
      <td>Salem</td>
      <td>DOG@co.marion.or.us</td>
      <td>503-588-5233</td>
      <td>OR</td>
      <td>...</td>
      <td>http://photos.petfinder.com/photos/pets/399528...</td>
      <td>F</td>
      <td>OR177</td>
      <td>17-1349</td>
      <td>L</td>
      <td>A</td>
      <td>hasShots</td>
      <td>altered</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
  </tbody>
</table>
<p>5 rows × 52 columns</p>
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
       'timestamp': {'$t': '2017-11-21T14:41:59Z'},
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
      <th>photos5</th>
      <th>photos6</th>
      <th>photos7</th>
      <th>photos8</th>
      <th>photos9</th>
      <th>photos10</th>
      <th>photos11</th>
      <th>photos12</th>
      <th>photos13</th>
      <th>photos14</th>
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
<p>1 rows × 39 columns</p>
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
      <td>Adult</td>
      <td>Dog</td>
      <td>Boxer</td>
      <td>Labrador Retriever</td>
      <td>NaN</td>
      <td>PO Box 60935</td>
      <td>Fort Myers</td>
      <td>rescueanimalsinneed@gmail.com</td>
      <td>407-414-2866</td>
      <td>FL</td>
      <td>...</td>
      <td>http://photos.petfinder.com/photos/pets/367743...</td>
      <td>F</td>
      <td>FL1027</td>
      <td>NaN</td>
      <td>M</td>
      <td>A</td>
      <td>hasShots</td>
      <td>noKids</td>
      <td>altered</td>
      <td>housetrained</td>
    </tr>
    <tr>
      <th>0</th>
      <td>Young</td>
      <td>Dog</td>
      <td>Beagle</td>
      <td>NaN</td>
      <td>Beagle</td>
      <td>P.O. Box 402</td>
      <td>Liberty Center</td>
      <td>heritagefarms08@gmail.com</td>
      <td>419-591-6621</td>
      <td>OH</td>
      <td>...</td>
      <td>http://photos.petfinder.com/photos/pets/391432...</td>
      <td>M</td>
      <td>OH743</td>
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
      <td>Domestic Short Hair</td>
      <td>NaN</td>
      <td>Domestic Short Hair</td>
      <td>NaN</td>
      <td>Kansas City</td>
      <td>coquina2@aol.com</td>
      <td>NaN</td>
      <td>MO</td>
      <td>...</td>
      <td>http://photos.petfinder.com/photos/pets/314172...</td>
      <td>M</td>
      <td>MO608</td>
      <td>NaN</td>
      <td>M</td>
      <td>A</td>
      <td>hasShots</td>
      <td>noDogs</td>
      <td>altered</td>
      <td>housetrained</td>
    </tr>
    <tr>
      <th>0</th>
      <td>Adult</td>
      <td>Cat</td>
      <td>Domestic Short Hair</td>
      <td>NaN</td>
      <td>Domestic Short Hair</td>
      <td>185 N Industrial Drive</td>
      <td>Erwin</td>
      <td>unicoicountyanimalshelter@gmail.com</td>
      <td>423-743-3071</td>
      <td>TN</td>
      <td>...</td>
      <td>http://photos.petfinder.com/photos/pets/394589...</td>
      <td>F</td>
      <td>TN489</td>
      <td>12046973</td>
      <td>M</td>
      <td>A</td>
      <td>altered</td>
      <td>housetrained</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>0</th>
      <td>Young</td>
      <td>Dog</td>
      <td>Rottweiler</td>
      <td>NaN</td>
      <td>Rottweiler</td>
      <td>3550 Aumsville Hwy SE</td>
      <td>Salem</td>
      <td>DOG@co.marion.or.us</td>
      <td>503-588-5233</td>
      <td>OR</td>
      <td>...</td>
      <td>http://photos.petfinder.com/photos/pets/399528...</td>
      <td>F</td>
      <td>OR177</td>
      <td>17-1349</td>
      <td>L</td>
      <td>A</td>
      <td>hasShots</td>
      <td>altered</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
  </tbody>
</table>
<p>5 rows × 52 columns</p>
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
      <td>Adult</td>
      <td>Dog</td>
      <td>Boxer</td>
      <td>Labrador Retriever</td>
      <td>NaN</td>
      <td>PO Box 60935</td>
      <td>Fort Myers</td>
      <td>rescueanimalsinneed@gmail.com</td>
      <td>407-414-2866</td>
      <td>FL</td>
      <td>...</td>
      <td>http://photos.petfinder.com/photos/pets/367743...</td>
      <td>F</td>
      <td>FL1027</td>
      <td>NaN</td>
      <td>M</td>
      <td>A</td>
      <td>hasShots</td>
      <td>noKids</td>
      <td>altered</td>
      <td>housetrained</td>
    </tr>
    <tr>
      <th>0</th>
      <td>Young</td>
      <td>Dog</td>
      <td>Beagle</td>
      <td>NaN</td>
      <td>Beagle</td>
      <td>P.O. Box 402</td>
      <td>Liberty Center</td>
      <td>heritagefarms08@gmail.com</td>
      <td>419-591-6621</td>
      <td>OH</td>
      <td>...</td>
      <td>http://photos.petfinder.com/photos/pets/391432...</td>
      <td>M</td>
      <td>OH743</td>
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
      <td>Domestic Short Hair</td>
      <td>NaN</td>
      <td>Domestic Short Hair</td>
      <td>NaN</td>
      <td>Kansas City</td>
      <td>coquina2@aol.com</td>
      <td>NaN</td>
      <td>MO</td>
      <td>...</td>
      <td>http://photos.petfinder.com/photos/pets/314172...</td>
      <td>M</td>
      <td>MO608</td>
      <td>NaN</td>
      <td>M</td>
      <td>A</td>
      <td>hasShots</td>
      <td>noDogs</td>
      <td>altered</td>
      <td>housetrained</td>
    </tr>
    <tr>
      <th>0</th>
      <td>Adult</td>
      <td>Cat</td>
      <td>Domestic Short Hair</td>
      <td>NaN</td>
      <td>Domestic Short Hair</td>
      <td>185 N Industrial Drive</td>
      <td>Erwin</td>
      <td>unicoicountyanimalshelter@gmail.com</td>
      <td>423-743-3071</td>
      <td>TN</td>
      <td>...</td>
      <td>http://photos.petfinder.com/photos/pets/394589...</td>
      <td>F</td>
      <td>TN489</td>
      <td>12046973</td>
      <td>M</td>
      <td>A</td>
      <td>altered</td>
      <td>housetrained</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>0</th>
      <td>Young</td>
      <td>Dog</td>
      <td>Rottweiler</td>
      <td>NaN</td>
      <td>Rottweiler</td>
      <td>3550 Aumsville Hwy SE</td>
      <td>Salem</td>
      <td>DOG@co.marion.or.us</td>
      <td>503-588-5233</td>
      <td>OR</td>
      <td>...</td>
      <td>http://photos.petfinder.com/photos/pets/399528...</td>
      <td>F</td>
      <td>OR177</td>
      <td>17-1349</td>
      <td>L</td>
      <td>A</td>
      <td>hasShots</td>
      <td>altered</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
  </tbody>
</table>
<p>5 rows × 52 columns</p>
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
       'timestamp': {'$t': '2017-11-22T16:00:53Z'},
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
pf.shelter_getPets(shelter_list[0], return_df=True)
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
      <th>breeds.breed</th>
      <th>contact.city</th>
      <th>contact.email</th>
      <th>contact.state</th>
      <th>contact.zip</th>
      <th>description</th>
      <th>id</th>
      <th>lastUpdate</th>
      <th>media.photos.photo</th>
      <th>mix</th>
      <th>name</th>
      <th>options.option</th>
      <th>options.option</th>
      <th>sex</th>
      <th>shelterId</th>
      <th>size</th>
      <th>status</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Adult</td>
      <td>Dog</td>
      <td>[{'$t': 'Shepherd'}, {'$t': 'Labrador Retrieve...</td>
      <td>NaN</td>
      <td>Auburn</td>
      <td>pugetsoundrescue@hotmail.com</td>
      <td>WA</td>
      <td>98092</td>
      <td>Morena is a shepherd/lab mix we are guessing, ...</td>
      <td>32080691</td>
      <td>2017-09-01T23:26:37Z</td>
      <td>[{'@size': 'pnt', '$t': 'http://photos.petfind...</td>
      <td>yes</td>
      <td>Morena</td>
      <td>[{'$t': 'hasShots'}, {'$t': 'altered'}, {'$t':...</td>
      <td>NaN</td>
      <td>F</td>
      <td>WA149</td>
      <td>M</td>
      <td>A</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Adult</td>
      <td>Dog</td>
      <td>[{'$t': 'Pit Bull Terrier'}, {'$t': 'Beagle'}]</td>
      <td>NaN</td>
      <td>Auburn</td>
      <td>pugetsoundrescue@hotmail.com</td>
      <td>WA</td>
      <td>98092</td>
      <td>Monty is a loving gentleman that likes long wa...</td>
      <td>34906970</td>
      <td>2017-09-01T23:26:59Z</td>
      <td>[{'@size': 'pnt', '$t': 'http://photos.petfind...</td>
      <td>yes</td>
      <td>Monty</td>
      <td>[{'$t': 'hasShots'}, {'$t': 'altered'}, {'$t':...</td>
      <td>NaN</td>
      <td>M</td>
      <td>WA149</td>
      <td>M</td>
      <td>A</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Adult</td>
      <td>Dog</td>
      <td>NaN</td>
      <td>Australian Cattle Dog / Blue Heeler</td>
      <td>Auburn</td>
      <td>pugetsoundrescue@hotmail.com</td>
      <td>WA</td>
      <td>98092</td>
      <td>ADOPTION DONATION: $350\n\nCONTACT US TODAY: P...</td>
      <td>37760609</td>
      <td>2017-11-01T05:01:56Z</td>
      <td>[{'@size': 'pnt', '$t': 'http://photos.petfind...</td>
      <td>yes</td>
      <td>Hobart</td>
      <td>[{'$t': 'hasShots'}, {'$t': 'altered'}, {'$t':...</td>
      <td>NaN</td>
      <td>M</td>
      <td>WA149</td>
      <td>M</td>
      <td>A</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Young</td>
      <td>Dog</td>
      <td>[{'$t': 'Pit Bull Terrier'}, {'$t': 'Labrador ...</td>
      <td>NaN</td>
      <td>Auburn</td>
      <td>pugetsoundrescue@hotmail.com</td>
      <td>WA</td>
      <td>98092</td>
      <td>ADOPTION DONATION: $350\n\nCONTACT US TODAY: P...</td>
      <td>38602092</td>
      <td>2017-09-01T21:00:13Z</td>
      <td>[{'@size': 'pnt', '$t': 'http://photos.petfind...</td>
      <td>yes</td>
      <td>Daughtry</td>
      <td>NaN</td>
      <td>hasShots</td>
      <td>M</td>
      <td>WA149</td>
      <td>M</td>
      <td>A</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Adult</td>
      <td>Dog</td>
      <td>NaN</td>
      <td>German Shepherd Dog</td>
      <td>Auburn</td>
      <td>pugetsoundrescue@hotmail.com</td>
      <td>WA</td>
      <td>98092</td>
      <td>ADOPTION DONATION: $350\n\nCONTACT US TODAY: P...</td>
      <td>38627371</td>
      <td>2017-11-20T13:54:50Z</td>
      <td>[{'@size': 'pnt', '$t': 'http://photos.petfind...</td>
      <td>no</td>
      <td>Poncho</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>M</td>
      <td>WA149</td>
      <td>L</td>
      <td>A</td>
    </tr>
    <tr>
      <th>5</th>
      <td>Adult</td>
      <td>Dog</td>
      <td>[{'$t': 'Husky'}, {'$t': 'Akita'}]</td>
      <td>NaN</td>
      <td>Auburn</td>
      <td>pugetsoundrescue@hotmail.com</td>
      <td>WA</td>
      <td>98092</td>
      <td>ADOPTION DONATION: $350\n\nCONTACT US TODAY: P...</td>
      <td>38899802</td>
      <td>2017-09-01T20:55:28Z</td>
      <td>[{'@size': 'pnt', '$t': 'http://photos.petfind...</td>
      <td>yes</td>
      <td>Cinder</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>F</td>
      <td>WA149</td>
      <td>L</td>
      <td>A</td>
    </tr>
    <tr>
      <th>6</th>
      <td>Adult</td>
      <td>Dog</td>
      <td>NaN</td>
      <td>German Shepherd Dog</td>
      <td>Auburn</td>
      <td>pugetsoundrescue@hotmail.com</td>
      <td>WA</td>
      <td>98092</td>
      <td>ADOPTION DONATION: $350\n\nCONTACT US TODAY: P...</td>
      <td>38900079</td>
      <td>2017-11-09T20:11:02Z</td>
      <td>[{'@size': 'pnt', '$t': 'http://photos.petfind...</td>
      <td>no</td>
      <td>Hercules</td>
      <td>[{'$t': 'hasShots'}, {'$t': 'altered'}]</td>
      <td>NaN</td>
      <td>M</td>
      <td>WA149</td>
      <td>L</td>
      <td>A</td>
    </tr>
    <tr>
      <th>7</th>
      <td>Adult</td>
      <td>Dog</td>
      <td>[{'$t': 'American Staffordshire Terrier'}, {'$...</td>
      <td>NaN</td>
      <td>Auburn</td>
      <td>pugetsoundrescue@hotmail.com</td>
      <td>WA</td>
      <td>98092</td>
      <td>ADOPTION DONATION: $350\n\nCONTACT US TODAY: P...</td>
      <td>38900083</td>
      <td>2017-09-01T20:51:06Z</td>
      <td>[{'@size': 'pnt', '$t': 'http://photos.petfind...</td>
      <td>yes</td>
      <td>Emily</td>
      <td>[{'$t': 'hasShots'}, {'$t': 'altered'}]</td>
      <td>NaN</td>
      <td>F</td>
      <td>WA149</td>
      <td>M</td>
      <td>A</td>
    </tr>
    <tr>
      <th>8</th>
      <td>Senior</td>
      <td>Dog</td>
      <td>NaN</td>
      <td>Cattle Dog</td>
      <td>Auburn</td>
      <td>pugetsoundrescue@hotmail.com</td>
      <td>WA</td>
      <td>98092</td>
      <td>ADOPTION DONATION: $350\n\nCONTACT US TODAY: P...</td>
      <td>38936726</td>
      <td>2017-09-01T23:30:27Z</td>
      <td>[{'@size': 'pnt', '$t': 'http://photos.petfind...</td>
      <td>yes</td>
      <td>Rex</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>M</td>
      <td>WA149</td>
      <td>M</td>
      <td>A</td>
    </tr>
    <tr>
      <th>9</th>
      <td>Senior</td>
      <td>Dog</td>
      <td>NaN</td>
      <td>Shepherd</td>
      <td>Auburn</td>
      <td>pugetsoundrescue@hotmail.com</td>
      <td>WA</td>
      <td>98092</td>
      <td>ADOPTION DONATION: $350\n\nCONTACT US TODAY: P...</td>
      <td>39229879</td>
      <td>2017-09-20T18:44:40Z</td>
      <td>[{'@size': 'pnt', '$t': 'http://photos.petfind...</td>
      <td>yes</td>
      <td>Fletch</td>
      <td>[{'$t': 'hasShots'}, {'$t': 'altered'}]</td>
      <td>NaN</td>
      <td>M</td>
      <td>WA149</td>
      <td>M</td>
      <td>A</td>
    </tr>
    <tr>
      <th>10</th>
      <td>Young</td>
      <td>Dog</td>
      <td>NaN</td>
      <td>German Shepherd Dog</td>
      <td>Auburn</td>
      <td>pugetsoundrescue@hotmail.com</td>
      <td>WA</td>
      <td>98092</td>
      <td>ADOPTION DONATION: $350\n\nCONTACT US TODAY: P...</td>
      <td>39229884</td>
      <td>2017-09-02T15:41:19Z</td>
      <td>[{'@size': 'pnt', '$t': 'http://photos.petfind...</td>
      <td>no</td>
      <td>Bear</td>
      <td>[{'$t': 'hasShots'}, {'$t': 'altered'}]</td>
      <td>NaN</td>
      <td>M</td>
      <td>WA149</td>
      <td>L</td>
      <td>A</td>
    </tr>
    <tr>
      <th>11</th>
      <td>Adult</td>
      <td>Dog</td>
      <td>[{'$t': 'Shar Pei'}, {'$t': 'Labrador Retrieve...</td>
      <td>NaN</td>
      <td>Auburn</td>
      <td>pugetsoundrescue@hotmail.com</td>
      <td>WA</td>
      <td>98092</td>
      <td>ADOPTION DONATION: $350\n\nCONTACT US TODAY: P...</td>
      <td>39229885</td>
      <td>2017-11-09T20:10:05Z</td>
      <td>[{'@size': 'pnt', '$t': 'http://photos.petfind...</td>
      <td>yes</td>
      <td>Beverly</td>
      <td>NaN</td>
      <td>hasShots</td>
      <td>F</td>
      <td>WA149</td>
      <td>M</td>
      <td>A</td>
    </tr>
    <tr>
      <th>12</th>
      <td>Senior</td>
      <td>Dog</td>
      <td>[{'$t': 'American Staffordshire Terrier'}, {'$...</td>
      <td>NaN</td>
      <td>Auburn</td>
      <td>pugetsoundrescue@hotmail.com</td>
      <td>WA</td>
      <td>98092</td>
      <td>ADOPTION DONATION: $350\n\nCONTACT US TODAY: P...</td>
      <td>39229895</td>
      <td>2017-09-02T15:25:55Z</td>
      <td>[{'@size': 'pnt', '$t': 'http://photos.petfind...</td>
      <td>yes</td>
      <td>Tripp</td>
      <td>[{'$t': 'hasShots'}, {'$t': 'altered'}, {'$t':...</td>
      <td>NaN</td>
      <td>M</td>
      <td>WA149</td>
      <td>M</td>
      <td>A</td>
    </tr>
    <tr>
      <th>13</th>
      <td>Adult</td>
      <td>Dog</td>
      <td>[{'$t': 'Siberian Husky'}, {'$t': 'Shetland Sh...</td>
      <td>NaN</td>
      <td>Auburn</td>
      <td>pugetsoundrescue@hotmail.com</td>
      <td>WA</td>
      <td>98092</td>
      <td>ADOPTION DONATION: $350\n\nCONTACT US TODAY: P...</td>
      <td>39414053</td>
      <td>2017-09-24T14:45:48Z</td>
      <td>[{'@size': 'pnt', '$t': 'http://photos.petfind...</td>
      <td>yes</td>
      <td>Penny</td>
      <td>[{'$t': 'hasShots'}, {'$t': 'altered'}, {'$t':...</td>
      <td>NaN</td>
      <td>F</td>
      <td>WA149</td>
      <td>M</td>
      <td>A</td>
    </tr>
    <tr>
      <th>14</th>
      <td>Young</td>
      <td>Dog</td>
      <td>[{'$t': 'Boxer'}, {'$t': 'American Staffordshi...</td>
      <td>NaN</td>
      <td>Auburn</td>
      <td>pugetsoundrescue@hotmail.com</td>
      <td>WA</td>
      <td>98092</td>
      <td>ADOPTION DONATION: $350\n\nCONTACT US TODAY: P...</td>
      <td>39414114</td>
      <td>2017-09-24T14:44:59Z</td>
      <td>[{'@size': 'pnt', '$t': 'http://photos.petfind...</td>
      <td>yes</td>
      <td>Hope</td>
      <td>[{'$t': 'hasShots'}, {'$t': 'altered'}, {'$t':...</td>
      <td>NaN</td>
      <td>F</td>
      <td>WA149</td>
      <td>M</td>
      <td>A</td>
    </tr>
    <tr>
      <th>15</th>
      <td>Adult</td>
      <td>Dog</td>
      <td>[{'$t': 'American Staffordshire Terrier'}, {'$...</td>
      <td>NaN</td>
      <td>Auburn</td>
      <td>pugetsoundrescue@hotmail.com</td>
      <td>WA</td>
      <td>98092</td>
      <td>ADOPTION DONATION: $350\n\nCONTACT US TODAY: P...</td>
      <td>39414121</td>
      <td>2017-09-23T23:20:28Z</td>
      <td>[{'@size': 'pnt', '$t': 'http://photos.petfind...</td>
      <td>yes</td>
      <td>Chata</td>
      <td>[{'$t': 'hasShots'}, {'$t': 'altered'}, {'$t':...</td>
      <td>NaN</td>
      <td>F</td>
      <td>WA149</td>
      <td>L</td>
      <td>A</td>
    </tr>
    <tr>
      <th>16</th>
      <td>Senior</td>
      <td>Dog</td>
      <td>NaN</td>
      <td>German Shepherd Dog</td>
      <td>Auburn</td>
      <td>pugetsoundrescue@hotmail.com</td>
      <td>WA</td>
      <td>98092</td>
      <td>We just took in Grady a few days ago.  Grady i...</td>
      <td>39793927</td>
      <td>2017-11-02T19:42:42Z</td>
      <td>[{'@size': 'pnt', '$t': 'http://photos.petfind...</td>
      <td>yes</td>
      <td>Grady</td>
      <td>[{'$t': 'hasShots'}, {'$t': 'altered'}]</td>
      <td>NaN</td>
      <td>M</td>
      <td>WA149</td>
      <td>L</td>
      <td>A</td>
    </tr>
    <tr>
      <th>17</th>
      <td>Senior</td>
      <td>Dog</td>
      <td>[{'$t': 'German Shepherd Dog'}, {'$t': 'Husky'}]</td>
      <td>NaN</td>
      <td>Auburn</td>
      <td>pugetsoundrescue@hotmail.com</td>
      <td>WA</td>
      <td>98092</td>
      <td>Bella is approximately 8 years old we are gues...</td>
      <td>39798015</td>
      <td>2017-11-02T19:43:24Z</td>
      <td>[{'@size': 'pnt', '$t': 'http://photos.petfind...</td>
      <td>yes</td>
      <td>Bella</td>
      <td>[{'$t': 'hasShots'}, {'$t': 'altered'}, {'$t':...</td>
      <td>NaN</td>
      <td>F</td>
      <td>WA149</td>
      <td>L</td>
      <td>A</td>
    </tr>
    <tr>
      <th>18</th>
      <td>Adult</td>
      <td>Dog</td>
      <td>NaN</td>
      <td>Doberman Pinscher</td>
      <td>Auburn</td>
      <td>pugetsoundrescue@hotmail.com</td>
      <td>WA</td>
      <td>98092</td>
      <td>Lancelot is a 2 year old purebred neutered mal...</td>
      <td>39798114</td>
      <td>2017-11-18T21:34:21Z</td>
      <td>[{'@size': 'pnt', '$t': 'http://photos.petfind...</td>
      <td>no</td>
      <td>Lancelot--ADOPTED!!</td>
      <td>[{'$t': 'hasShots'}, {'$t': 'altered'}]</td>
      <td>NaN</td>
      <td>M</td>
      <td>WA149</td>
      <td>L</td>
      <td>A</td>
    </tr>
    <tr>
      <th>19</th>
      <td>Young</td>
      <td>Cat</td>
      <td>NaN</td>
      <td>Domestic Short Hair (Gray &amp; White)</td>
      <td>Auburn</td>
      <td>pugetsoundrescue@hotmail.com</td>
      <td>WA</td>
      <td>98092</td>
      <td>NaN</td>
      <td>39898075</td>
      <td>2017-11-13T16:50:44Z</td>
      <td>[{'@size': 'pnt', '$t': 'http://photos.petfind...</td>
      <td>no</td>
      <td>Momma kitty</td>
      <td>[{'$t': 'hasShots'}, {'$t': 'altered'}, {'$t':...</td>
      <td>NaN</td>
      <td>F</td>
      <td>WA149</td>
      <td>M</td>
      <td>A</td>
    </tr>
    <tr>
      <th>20</th>
      <td>Baby</td>
      <td>Cat</td>
      <td>NaN</td>
      <td>Domestic Medium Hair (Gray &amp; White)</td>
      <td>Auburn</td>
      <td>pugetsoundrescue@hotmail.com</td>
      <td>WA</td>
      <td>98092</td>
      <td>NaN</td>
      <td>39898092</td>
      <td>2017-11-13T16:51:53Z</td>
      <td>[{'@size': 'pnt', '$t': 'http://photos.petfind...</td>
      <td>no</td>
      <td>Baby kittens!</td>
      <td>[{'$t': 'hasShots'}, {'$t': 'housetrained'}]</td>
      <td>NaN</td>
      <td>M</td>
      <td>WA149</td>
      <td>M</td>
      <td>A</td>
    </tr>
    <tr>
      <th>21</th>
      <td>Young</td>
      <td>Dog</td>
      <td>NaN</td>
      <td>German Shepherd Dog</td>
      <td>Auburn</td>
      <td>pugetsoundrescue@hotmail.com</td>
      <td>WA</td>
      <td>98092</td>
      <td>ADOPTION DONATION: $350\n\nCONTACT US TODAY: P...</td>
      <td>39898105</td>
      <td>2017-11-16T14:03:18Z</td>
      <td>[{'@size': 'pnt', '$t': 'http://photos.petfind...</td>
      <td>no</td>
      <td>Duke</td>
      <td>[{'$t': 'hasShots'}, {'$t': 'altered'}]</td>
      <td>NaN</td>
      <td>M</td>
      <td>WA149</td>
      <td>L</td>
      <td>A</td>
    </tr>
    <tr>
      <th>22</th>
      <td>Young</td>
      <td>Dog</td>
      <td>NaN</td>
      <td>German Shepherd Dog</td>
      <td>Auburn</td>
      <td>pugetsoundrescue@hotmail.com</td>
      <td>WA</td>
      <td>98092</td>
      <td>ADOPTION DONATION: $350\n\nCONTACT US TODAY: P...</td>
      <td>39898144</td>
      <td>2017-11-16T14:02:30Z</td>
      <td>[{'@size': 'pnt', '$t': 'http://photos.petfind...</td>
      <td>no</td>
      <td>Wrigley</td>
      <td>[{'$t': 'hasShots'}, {'$t': 'altered'}]</td>
      <td>NaN</td>
      <td>M</td>
      <td>WA149</td>
      <td>L</td>
      <td>A</td>
    </tr>
    <tr>
      <th>23</th>
      <td>Adult</td>
      <td>Dog</td>
      <td>[{'$t': 'Beagle'}, {'$t': 'Basset Hound'}]</td>
      <td>NaN</td>
      <td>Auburn</td>
      <td>pugetsoundrescue@hotmail.com</td>
      <td>WA</td>
      <td>98092</td>
      <td>ADOPTION DONATION: $350\n\nCONTACT US TODAY: P...</td>
      <td>39899592</td>
      <td>2017-11-16T14:02:12Z</td>
      <td>[{'@size': 'pnt', '$t': 'http://photos.petfind...</td>
      <td>yes</td>
      <td>Beau</td>
      <td>[{'$t': 'hasShots'}, {'$t': 'altered'}, {'$t':...</td>
      <td>NaN</td>
      <td>M</td>
      <td>WA149</td>
      <td>M</td>
      <td>A</td>
    </tr>
    <tr>
      <th>24</th>
      <td>Young</td>
      <td>Dog</td>
      <td>NaN</td>
      <td>German Shepherd Dog</td>
      <td>Auburn</td>
      <td>pugetsoundrescue@hotmail.com</td>
      <td>WA</td>
      <td>98092</td>
      <td>ADOPTION DONATION: $350\n\nCONTACT US TODAY: P...</td>
      <td>39899643</td>
      <td>2017-11-16T14:01:56Z</td>
      <td>[{'@size': 'pnt', '$t': 'http://photos.petfind...</td>
      <td>no</td>
      <td>Brody</td>
      <td>[{'$t': 'hasShots'}, {'$t': 'altered'}]</td>
      <td>NaN</td>
      <td>M</td>
      <td>WA149</td>
      <td>L</td>
      <td>A</td>
    </tr>
  </tbody>
</table>
</div>



<a id='shelter.listByBreed'></a>

### Finding shelters that have records matching a particular animal breed

The `shelter_listByBreeds()` method allows the user to find shelters that match pet records of the input animal breed. This method is best used in conjunction with the `breed_list()` method to find the available animal breeds in the Petfinder database.

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
pf.shelter_listByBreed('cat', aby, return_df=True)
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
    <tr>
      <th>5</th>
      <td>2656 Hwy. 201 N</td>
      <td>NaN</td>
      <td>Mountain Home</td>
      <td>US</td>
      <td>hsnca@mtnhome.com</td>
      <td>AR95</td>
      <td>36.3383</td>
      <td>-92.3742</td>
      <td>Humane Society of North Central Arkansas</td>
      <td>(870) 425-9221</td>
      <td>AR</td>
      <td>72653</td>
    </tr>
    <tr>
      <th>6</th>
      <td>NaN</td>
      <td>NaN</td>
      <td>Phoenix</td>
      <td>US</td>
      <td>badkittyts@aol.com</td>
      <td>AZ01</td>
      <td>33.9158</td>
      <td>-112.1353</td>
      <td>Citizens For North Phoenix Strays</td>
      <td>(602) 332-6615</td>
      <td>AZ</td>
      <td>85027</td>
    </tr>
    <tr>
      <th>7</th>
      <td>835 West Warner Road</td>
      <td>NaN</td>
      <td>Gilbert</td>
      <td>US</td>
      <td>azcatsmeow@gmail.com</td>
      <td>AZ13</td>
      <td>33.3557</td>
      <td>-111.7917</td>
      <td>We're The Cat's Meow Pet Rescue</td>
      <td>480-278-9744</td>
      <td>AZ</td>
      <td>85233</td>
    </tr>
    <tr>
      <th>8</th>
      <td>P.O Box 50673</td>
      <td>NaN</td>
      <td>Phoenix</td>
      <td>US</td>
      <td>petfinder-inquiry@cactuscatsrescue.net</td>
      <td>AZ258</td>
      <td>33.3357</td>
      <td>-111.9924</td>
      <td>Cactus Cats Rescue, Inc.</td>
      <td>(480) 814-8801</td>
      <td>AZ</td>
      <td>85044</td>
    </tr>
    <tr>
      <th>9</th>
      <td>P.O. Box 50594</td>
      <td>NaN</td>
      <td>Mesa</td>
      <td>US</td>
      <td>hadleyd@cox.net</td>
      <td>AZ301</td>
      <td>33.4007</td>
      <td>-111.6539</td>
      <td>Desert Paws Rescue</td>
      <td>480-380-5214</td>
      <td>AZ</td>
      <td>85208</td>
    </tr>
    <tr>
      <th>10</th>
      <td>NaN</td>
      <td>NaN</td>
      <td>Phoenix</td>
      <td>US</td>
      <td>vlintz@davisp.com</td>
      <td>AZ324</td>
      <td>33.4483</td>
      <td>-112.0733</td>
      <td>The Litter League (Rescue League)</td>
      <td>NaN</td>
      <td>AZ</td>
      <td>85064</td>
    </tr>
    <tr>
      <th>11</th>
      <td>5278 East 21st Street</td>
      <td>NaN</td>
      <td>Tucson</td>
      <td>US</td>
      <td>adoptions@hermitagecatshelter.org</td>
      <td>AZ70</td>
      <td>32.2152</td>
      <td>-110.8853</td>
      <td>The Hermitage Cat Shelter</td>
      <td>520-571-7839</td>
      <td>AZ</td>
      <td>85711</td>
    </tr>
    <tr>
      <th>12</th>
      <td>NaN</td>
      <td>NaN</td>
      <td>Ahwatukee</td>
      <td>US</td>
      <td>ajbfcats@gmail.com</td>
      <td>AZ88</td>
      <td>33.3557</td>
      <td>-111.7917</td>
      <td>AJs Best Friends Persian &amp; Himalayan Rescue</td>
      <td>NaN</td>
      <td>AZ</td>
      <td>85233</td>
    </tr>
    <tr>
      <th>13</th>
      <td>P.O. Box 494274</td>
      <td>Redding, CA 96049-4274</td>
      <td>Palo Cedro</td>
      <td>US</td>
      <td>acawl.inc@gmail.com</td>
      <td>CA1004</td>
      <td>40.5713</td>
      <td>-122.2371</td>
      <td>Another Chance Animal Welfare League Inc.</td>
      <td>530-547-7387</td>
      <td>CA</td>
      <td>96073</td>
    </tr>
    <tr>
      <th>14</th>
      <td>NaN</td>
      <td>NaN</td>
      <td>Santa Rosa</td>
      <td>US</td>
      <td>Asmcmvw@aol.com</td>
      <td>CA1043</td>
      <td>38.4434</td>
      <td>-122.7511</td>
      <td>Purrfect Pals</td>
      <td>NaN</td>
      <td>CA</td>
      <td>95401</td>
    </tr>
    <tr>
      <th>15</th>
      <td>NaN</td>
      <td>NaN</td>
      <td>Napa</td>
      <td>US</td>
      <td>wtfnapa@gmail.com</td>
      <td>CA1328</td>
      <td>38.3265</td>
      <td>-122.3044</td>
      <td>Whiskers, Tails and Ferals</td>
      <td>(707) 258-2287</td>
      <td>CA</td>
      <td>94558</td>
    </tr>
    <tr>
      <th>16</th>
      <td>361 S. Raymond Avenue</td>
      <td>NaN</td>
      <td>Pasadena</td>
      <td>US</td>
      <td>NaN</td>
      <td>CA15</td>
      <td>34.1363</td>
      <td>-118.1653</td>
      <td>Pasadena Humane Society &amp; SPCA</td>
      <td>626-792-7151</td>
      <td>CA</td>
      <td>91105</td>
    </tr>
    <tr>
      <th>17</th>
      <td>359 Nevada Street, Suite 101</td>
      <td>NaN</td>
      <td>Auburn</td>
      <td>US</td>
      <td>sahartford530@gmail.com</td>
      <td>CA1505</td>
      <td>38.8967</td>
      <td>-121.0758</td>
      <td>Friends Forever, A Cat Sanctuary</td>
      <td>530-885-4228</td>
      <td>CA</td>
      <td>95604</td>
    </tr>
    <tr>
      <th>18</th>
      <td>P.O. Box 510</td>
      <td>NaN</td>
      <td>Davis</td>
      <td>US</td>
      <td>adopt@yolospca.org</td>
      <td>CA161</td>
      <td>38.545</td>
      <td>-121.7394</td>
      <td>Yolo County SPCA</td>
      <td>NaN</td>
      <td>CA</td>
      <td>95617</td>
    </tr>
    <tr>
      <th>19</th>
      <td>NaN</td>
      <td>NaN</td>
      <td>Buena Park</td>
      <td>US</td>
      <td>CaringFriendsCatRescueTustin@gmail.Com</td>
      <td>CA1721</td>
      <td>33.8763</td>
      <td>-117.9903</td>
      <td>Caring Friends Cat Rescue</td>
      <td>NaN</td>
      <td>CA</td>
      <td>90621</td>
    </tr>
    <tr>
      <th>20</th>
      <td>420 McKinley St, Ste 111-147</td>
      <td>NaN</td>
      <td>Corona</td>
      <td>US</td>
      <td>purrfectfit2000-rescue@yahoo.com</td>
      <td>CA1723</td>
      <td>33.8781</td>
      <td>-117.5814</td>
      <td>Purrfect Fit Cat Rescue</td>
      <td>951-817-9545</td>
      <td>CA</td>
      <td>92879</td>
    </tr>
    <tr>
      <th>21</th>
      <td>NaN</td>
      <td>NaN</td>
      <td>Panorama City</td>
      <td>US</td>
      <td>gduncan13@gmail.com</td>
      <td>CA1752</td>
      <td>34.2242</td>
      <td>-118.4433</td>
      <td>HA! Inc.</td>
      <td>NaN</td>
      <td>CA</td>
      <td>91402</td>
    </tr>
    <tr>
      <th>22</th>
      <td>5473 Overpass Rd</td>
      <td>NaN</td>
      <td>Santa Barbara</td>
      <td>US</td>
      <td>info@asapcats.org</td>
      <td>CA267</td>
      <td>34.4427</td>
      <td>-119.8024</td>
      <td>Animal Shelter Assistance Program (ASAP)</td>
      <td>(805) 683-3368</td>
      <td>CA</td>
      <td>93111</td>
    </tr>
    <tr>
      <th>23</th>
      <td>P.O. Box 2011</td>
      <td>NaN</td>
      <td>Antioch</td>
      <td>US</td>
      <td>starshalodogs@yahoo.com</td>
      <td>CA338</td>
      <td>38.005</td>
      <td>-121.8047</td>
      <td>Homeless Animals' Lifeline Organization (H.A.L...</td>
      <td>(925) 473-4642</td>
      <td>CA</td>
      <td>94531</td>
    </tr>
    <tr>
      <th>24</th>
      <td>3839 Bradshaw Road</td>
      <td>NaN</td>
      <td>Sacramento</td>
      <td>US</td>
      <td>CountyAnimalCare@saccounty.net</td>
      <td>CA348</td>
      <td>38.5655</td>
      <td>-121.3283</td>
      <td>Sacramento County Animal Care and Regulation</td>
      <td>CountyAnimalCare@saccounty.net</td>
      <td>CA</td>
      <td>95827</td>
    </tr>
  </tbody>
</table>
</div>

