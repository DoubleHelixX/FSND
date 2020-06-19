#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
# migration file import - manage.py class can alternately run as a script instead as well
import manage as m
import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for, jsonify
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import FlaskForm
from forms import *
from colorama import Fore , Style
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)

# BOOTSTRAP DB migration command with migration file
migration = m.migration(app, db)

# TODO: connect to a local postgresql database

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#


class Venue(db.Model):
    __tablename__ = 'venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String(120))) 
    website_link = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean, default = False)
    seeking_description = db.Column(db.String(250))
    num_of_shows = db.Column(db.Integer, default = 0)
    shows = db.relationship('Show', backref='venue', lazy=True)
    deleted = db.Column(db.Boolean, default = False)
    
    def __repr__(self):
      return f'<Venue {self.id} {self.name}>'
    
    
class Artist(db.Model):
    __tablename__ = 'artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String(120)))
    image_link = db.Column(db.String(500))
    website_link = db.Column(db.String(120))
    facebook_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean, default = False)
    seeking_description = db.Column(db.String(250))
    num_of_shows = db.Column(db.Integer, default = 0)
    shows = db.relationship('Show', backref='artist', lazy=True)
    deleted = db.Column(db.Boolean, default = False)
    
    def __repr__(self):
      return f'<Artist {self.id} {self.name}>'

  

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.
class Show(db.Model):
  __tablename__ = 'shows'
  id = db.Column(db.Integer, primary_key=True)
  artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), nullable=False)
  venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'), nullable=False)
  start_time = db.Column(db.DateTime, nullable=False)
  deleted = db.Column(db.Boolean, default = False)
  
  

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#


def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format = "EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format = "EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)


app.jinja_env.filters['datetime'] = format_datetime

def manageSequence(tableName,className):
  #COUNT METHODS - DIFFERENT APPROACHES BECAUSE COUNT() TAKES TO LONG IN LARGE DB - ***REVISION LATER***
  #maxCount = select([func.count()]).select_from(Todo)
  maxCount = db.session.query(className).all().count(className.id)
  #print(maxCount)
  #Reset the auto PK increment sequence to current max
  alterSeq= "ALTER SEQUENCE " + tableName +"_id_seq RESTART WITH " + str(maxCount) #substitute for 1 if starting off empty with todos
  print(alterSeq, 'OGMAGODA')
  db.session.execute(alterSeq)
  db.session.commit()
  db.session.close()  
  
  
#manageSequence("venue",Venue)
#manageSequence("artist",Artist)
#manageSequence("shows", Show)
#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#


@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  error=False
  try:
    #maxCount = db.session.query(Venue.id).count()
    #print("maxCount", maxCount)
    mockData = [{
    "city": "San Francisco",
    "state": "CA",
    "venues": [{
      "id": 1,
      "name": "The Musical Hop",
      "num_upcoming_shows": 0,
    }, {
      "id": 3,
      "name": "Park Square Live Music & Coffee",
      "num_upcoming_shows": 1,
    }]
    }, {
    "city": "New York",
    "state": "NY",
    "venues": [{
      "id": 2,
      "name": "The Dueling Pianos Bar",
      "num_upcoming_shows": 0,
    }]
    }]
    
    returnData = []
    dbData = db.session.query(Venue).filter(Venue.deleted == False).order_by('id').all()
    rowArryCheck = []
    areaData = []
    venuesData = []
    error=False
    
    #print('data2: ', dbData)
    for row in dbData:
      #print('rowindy: ' , rowIndex)
      rowIndex=0
      cityData=0
      print(f'{Fore.YELLOW} omgg :')
      venueListings = Venue.query.filter(Venue.state==row.state).filter(Venue.city == row.city).filter(Venue.deleted==False).order_by('id').all()
      print(f'{Fore.YELLOW} Venuelisting :  ' , venueListings)
      for i in venueListings:
        upcoming_shows = 0
        matchedVenues = Show.query.filter(Show.venue_id == i.id).filter(Show.deleted==False).all()
        if(matchedVenues):
          for venues in matchedVenues:
            if venues.start_time > datetime.today(): upcoming_shows =+1      
        if ((i.id in rowArryCheck) == False):
          rowArryCheck.append(i.id)
          if(rowIndex>0):
            if((i.city) in areaData):
                venuesData.append({
                "city": "",
                "state": "",
                "venues":[{
                "id": i.id,
                "name": i.name,
                "num_upcoming_shows": upcoming_shows,
              }]
                })
            else:
                venuesData.append({
                "city": i.city,
                "state": i.state, # place as null to only show city
                "venues":[{
                "id": i.id,
                "name": i.name,
                "num_upcoming_shows": upcoming_shows,
              }]
                })
                areaData.append(i.city)
                print("after",areaData)
          else:
            venuesData.append({
            "city": i.city,
            "state": i.state,
            "venues":[{
            "id": i.id,
            "name": i.name,
            "num_upcoming_shows": upcoming_shows,
            }]
            })
            areaData.append(i.city)
            rowIndex=rowIndex+1
  except():
    flash('An error occurred listing the Venues. Redirecting to home page')
    error =True
  finally:
    if(error):
      return redirect(url_for("index"))
    else:
      return render_template('pages/venues.html', areas=venuesData)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  error=False
  try:
    mockData={
      "count": 1,
      "data": [{
        "id": 2,
        "name": "The Dueling Pianos Bar",
        "num_upcoming_shows": 0,
      }]
    }
    # Get search value from form
    searchTerm = request.form.get('search_term','').lower()
    print(f'{Fore.RED} Search Term: ' , searchTerm)
    perfectMatch =[]
    goodMatch=[]
    poorMatch=[]
    unfilteredMatch=[]
    count=0
    for row in db.session.query(Venue).filter(Venue.deleted==False).all():
      upcoming_shows = 0
      matchedVenues = Show.query.filter(Show.venue_id == row.id).all()
      if(matchedVenues):
        for venues in matchedVenues:
          if venues.start_time > datetime.today(): upcoming_shows =+1
      if(row.name.lower() == searchTerm or row.name.lower().startswith(searchTerm)):
        unfilteredMatch.append({
        "id": row.id,
        "name": row.name.title(),
        "num_upcoming_shows": upcoming_shows
        })
        count = count+1
    searchResult={
      "count": count,
      "data": unfilteredMatch
    }
  except:
    flash('An error occurred when searching for ', searchTerm )
    print(sys.exc_info())
  finally:
    db.session.close()
    if(error):
      return redirect(url_for('venues'))
    else:
      return render_template('pages/search_venues.html', results=searchResult, search_term=searchTerm)

  

  

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  error=True
  try:
    data1={
    "id": 1,
    "name": "The Musical Hop",
    "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
    "address": "1015 Folsom Street",
    "city": "San Francisco",
    "state": "CA",
    "phone": "123-123-1234",
    "website": "https://www.themusicalhop.com",
    "facebook_link": "https://www.facebook.com/TheMusicalHop",
    "seeking_talent": True,
    "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
    "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
    "past_shows": [{ # check show table and match show_venue id with venue_id where start_time < current date
      "artist_id": 4, # match artist_id associated with particular venue_id row and get data below from arist table
      "artist_name": "Guns N Petals",
      "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
      "start_time": "2019-05-21T21:30:00.000Z" # get start_time from show table and match show_venue id with venue_id
    }],
    "upcoming_shows": [], ## check show table and match show_venue id with venue_id where start_time > current date
    "past_shows_count": 1, #count checked query
    "upcoming_shows_count": 0, #count checked query
    }
    data2={
    "id": 2,
    "name": "The Dueling Pianos Bar",
    "genres": ["Classical", "R&B", "Hip-Hop"],
    "address": "335 Delancey Street",
    "city": "New York",
    "state": "NY",
    "phone": "914-003-1132",
    "website": "https://www.theduelingpianos.com",
    "facebook_link": "https://www.facebook.com/theduelingpianos",
    "seeking_talent": False,
    "image_link": "https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80",
    "past_shows": [],
    "upcoming_shows": [],
    "past_shows_count": 0,
    "upcoming_shows_count": 0,
    }
    data3={
    "id": 3,
    "name": "Park Square Live Music & Coffee",
    "genres": ["Rock n Roll", "Jazz", "Classical", "Folk"],
    "address": "34 Whiskey Moore Ave",
    "city": "San Francisco",
    "state": "CA",
    "phone": "415-000-1234",
    "website": "https://www.parksquarelivemusicandcoffee.com",
    "facebook_link": "https://www.facebook.com/ParkSquareLiveMusicAndCoffee",
    "seeking_talent": False,
    "image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
    "past_shows": [{
      "artist_id": 5,
      "artist_name": "Matt Quevedo",
      "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
      "start_time": "2019-06-15T23:00:00.000Z"
    }],
    "upcoming_shows": [{
      "artist_id": 6,
      "artist_name": "The Wild Sax Band",
      "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
      "start_time": "2035-04-01T20:00:00.000Z"
    }, {
      "artist_id": 6,
      "artist_name": "The Wild Sax Band",
      "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
      "start_time": "2035-04-08T20:00:00.000Z"
    }, {
      "artist_id": 6,
      "artist_name": "The Wild Sax Band",
      "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
      "start_time": "2035-04-15T20:00:00.000Z"
    }],
    "past_shows_count": 1,
    "upcoming_shows_count": 1,
    }
    resultData=[]
    venueData = db.session.query(Venue).filter(Venue.deleted == False).all()
    for venue in venueData:
      pastShowsCount =0
      upcomingShowsCount=0
      pastShows=[]
      upcomingShows=[]
      genres="".join(list(filter(lambda x : x!= '{' and x!='}', venue.genres ))).split(',')
      if venue.num_of_shows >0:
        showsData = db.session.query(Show, Artist).filter(Show.venue_id == venue.id).filter(Artist.id == Show.artist_id).all()
        for shows in showsData:
          print(f'{Fore.YELLOW} shows: {shows}')
          if shows[0].start_time > datetime.today(): 
            upcomingShowsCount +=1
            upcomingShows.append({
            "artist_id": shows[1].id,
            "artist_name": shows[1].name,
            "artist_image_link": shows[1].image_link,
            "start_time": str(shows[0].start_time)
            })
          else: 
            pastShowsCount +=1
            pastShows.append({
              "artist_id": shows[1].id,
              "artist_name": shows[1].name,
              "artist_image_link": shows[1].image_link,
              "start_time": str(shows[0].start_time)
              
            })
        
        resultData.append({
          "id": venue.id,
          "name": venue.name,
          "genres": genres,
          "address": venue.address,
          "city": venue.city,
          "state": venue.state,
          "phone": venue.phone,
          "website":venue.website_link,
          "facebook_link": venue.facebook_link,
          "seeking_talent": venue.seeking_talent,
          "seeking_description":venue.seeking_description,
          "image_link": venue.image_link,
          "past_shows": pastShows,
          "upcoming_shows": upcomingShows,
          "past_shows_count": pastShowsCount,
          "upcoming_shows_count": upcomingShowsCount, 
        })  
      else:
        resultData.append({
          "id": venue.id,
          "name": venue.name,
          "genres": genres,
          "address": venue.address,
          "city": venue.city,
          "state": venue.state,
          "phone": venue.phone,
          "website":venue.website_link,
          "facebook_link": venue.facebook_link,
          "seeking_talent": venue.seeking_talent,
          "seeking_description":venue.seeking_description,
          "image_link": venue.image_link,
          "past_shows": pastShows,
          "upcoming_shows": upcomingShows,
          "past_shows_count": pastShowsCount,
          "upcoming_shows_count": upcomingShowsCount, 
        }) 
    error=False 
    data = list(filter(lambda d: d['id'] == venue_id, resultData))[0] #works with 1 dictionary obj
  except expression as identifier:
    error=True
    print(f'{Fore.Yellow} Error Message: ' , identifier)
    flash('Error when accessing Database: Contact Customer Support if issue persist.')
  finally:
    if error: redirect(url_for('index'))
    else: return render_template('pages/show_venue.html', venue=data)
    
  

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  error=False
  try:
    form = VenueForm(request.form)
    # retrieve the form values
    vName=form.name.data
    vCity=form.city.data.title()
    vState=form.state.data
    vAddress=form.address.data
    vPhone=form.phone.data
    vGenres=form.genres.data
    vWebsite_link = form.website_link.data
    vImage_link=form.image_link.data
    vFacebook_link=form.facebook_link.data
    vSeeking_description=form.seeking_description.data
    #Retrieve BooleanField values and test them. work around hack - BooleanField is buggy
    try:
      #If it can't read it and causes error its not clicked indicating false
      vSeeking_talent= form.seeking_talent.data
    except:
      #set it to false
      vSeeking_talent=False
    finally:
      #if the return value is 'y' or anything else other than a bool then set to true
      if (isinstance(vSeeking_talent, bool) == False):
        vSeeking_talent=True
                
    # TODO: insert form data as a new Venue record in the db, instead
    newVenue = Venue(name=vName, city=vCity , state=vState, address=vAddress, phone=vPhone, genres=vGenres, image_link=vImage_link, facebook_link=vFacebook_link,seeking_talent=vSeeking_talent, seeking_description=vSeeking_description, website_link = vWebsite_link )
    # print('Printing new venue obj: ' ,newVenue , ' || ' ,newVenue.query.all())
    # TODO: modify data to be the data object returned from db insertion
    db.session.add(newVenue)
    # on successful db insert, flash success
    db.session.commit()
    flash('Venue ' + vName + ' was successfully listed!')
  except:
    error=True
    db.session.rollback()
    print(sys.exc_info())
    # TODO: on unsuccessful db insert, flash an error instead.
    flash('An error occurred. Venue ' + vName + ' could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  finally:
    db.session.close()
    if error: return redirect(url_for('create_venue_submission'))
    else: return redirect(url_for('index'))

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    # TODO: Complete this endpoint for taking a venue_id, and using
    # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
 try:
    toBeDeleted = db.session.query(Venue).filter_by(id=venue_id).all()
    toBeDeleted[0].deleted=True
    # commit delete changes before updating sequence
    db.session.commit()
    flash('Venue Deleted')
 except:
    print('Could not delete: ' ,venue_id)
    flash('An error occurred. Venue could not be deleted.')
    print(sys.exc_info())
    db.session.rollback()
 finally:
    db.session.close()
    return jsonify({"redirect": "/"})
   
  
@app.route('/artist/<artist_id>', methods=['DELETE'])
def delete_artist(artist_id):
    # TODO: Complete this endpoint for taking a venue_id, and using
    # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
 try:
    # Delete clicked selection of Todo list
    #Venue.query.filter(id = venue_id).delete()
    toBeDeleted = db.session.query(Artist).filter_by(id=artist_id).all()
    toBeDeleted[0].deleted=True
    # commit delete changes before updating sequence
    db.session.commit()
    flash('Artist Deleted')
 except:
    print('Could not delete: ' ,artist_id)
    flash('An error occurred. Artist could not be deleted.')
    print(sys.exc_info())
    db.session.rollback()
 finally:
    db.session.close()
    return jsonify({"redirect": "/"})

#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  try:
    mockData=[{
    "id": 4,
    "name": "Guns N Petals",
    }, {
    "id": 5,
    "name": "Matt Quevedo",
    }, {
    "id": 6,
    "name": "The Wild Sax Band",
    }]
    returnData=[]
    allArtist= Artist.query.filter(Artist.deleted==False).order_by('id').all()
    for artist in allArtist:
      data= {
      "id": artist.id,
      "name": artist.name
      }
      returnData.append(data)
  except:
    print(f'{Fore.RED} Error: ', sys.exc_info())
  finally:
    return render_template('pages/artists.html', artists=returnData)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  # Get search value from form
  try:
    mockData={
    "count": 1,
    "data": [{
      "id": 4,
      "name": "Guns N Petals",
      "num_upcoming_shows": 0,
    }]
    }
    # Get search value from form
    searchTerm = request.form.get('search_term','').lower()
    print(f'{Fore.RED} Search Term: ' , searchTerm)
    perfectMatch =[]
    goodMatch=[]
    poorMatch=[]
    unfilteredMatch=[]
    count=0
    for row in db.session.query(Artist).filter(Artist.deleted==False).all():
      upcoming_shows = 0
      matchedVenues = Show.query.filter(Show.venue_id == row.id).all()
      if(matchedVenues):
        for venues in matchedVenues:
          if venues.start_time > datetime.today(): upcoming_shows =+1
      if(row.name.lower() == searchTerm or row.name.lower().startswith(searchTerm)):
        unfilteredMatch.append({
        "id": row.id,
        "name": row.name.title(),
        "num_upcoming_shows": upcoming_shows
      })
        count = count+1
    
    searchResult={
      "count": count,
      "data": unfilteredMatch
    } 
  except:
    flash('An error occurred when searching for ', searchTerm )
    print(sys.exc_info())
  finally:
    db.session.close()
    return render_template('pages/search_artists.html', results=searchResult, search_term=searchTerm)
  return redirect(url_for('artists'))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  error =True
  try:
    resultData=[]
    data1={
      "id": 4,
      "name": "Guns N Petals",
      "genres": ["Rock n Roll"],
      "city": "San Francisco",
      "state": "CA",
      "phone": "326-123-5000",
      "website": "https://www.gunsnpetalsband.com",
      "facebook_link": "https://www.facebook.com/GunsNPetals",
      "seeking_venue": True,
      "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
      "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
      "past_shows": [{
        "venue_id": 1,
        "venue_name": "The Musical Hop",
        "venue_image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
        "start_time": "2019-05-21T21:30:00.000Z"
      }],
      "upcoming_shows": [],
      "past_shows_count": 1,
      "upcoming_shows_count": 0,
    }
    data2={
      "id": 5,
      "name": "Matt Quevedo",
      "genres": ["Jazz"],
      "city": "New York",
      "state": "NY",
      "phone": "300-400-5000",
      "facebook_link": "https://www.facebook.com/mattquevedo923251523",
      "seeking_venue": False,
      "image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
      "past_shows": [{
        "venue_id": 3,
        "venue_name": "Park Square Live Music & Coffee",
        "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
        "start_time": "2019-06-15T23:00:00.000Z"
      }],
      "upcoming_shows": [],
      "past_shows_count": 1,
      "upcoming_shows_count": 0,
    }
    data3={
      "id": 6,
      "name": "The Wild Sax Band",
      "genres": ["Jazz", "Classical"],
      "city": "San Francisco",
      "state": "CA",
      "phone": "432-325-5432",
      "seeking_venue": False,
      "image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
      "past_shows": [],
      "upcoming_shows": [{
        "venue_id": 3,
        "venue_name": "Park Square Live Music & Coffee",
        "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
        "start_time": "2035-04-01T20:00:00.000Z"
      }, {
        "venue_id": 3,
        "venue_name": "Park Square Live Music & Coffee",
        "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
        "start_time": "2035-04-08T20:00:00.000Z"
      }, {
        "venue_id": 3,
        "venue_name": "Park Square Live Music & Coffee",
        "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
        "start_time": "2035-04-15T20:00:00.000Z"
      }],
      "past_shows_count": 0,
      "upcoming_shows_count": 3,
    }
    
    artistsData = db.session.query(Artist).filter(Artist.deleted == False).all()
    for artist in artistsData:
      pastShowsCount =0
      upcomingShowsCount=0
      pastShows=[]
      upcomingShows=[]
      genres=''.join(list(filter(lambda x : x!= '{' and x!='}' and x!='"', artist.genres ))).split(',')
      
      if artist.num_of_shows >0:
        showsData = db.session.query(Show, Venue).filter(Show.artist_id == artist.id).filter(Venue.id == Show.venue_id).all()
        for shows in showsData:
          print(f'{Fore.YELLOW} shows: {shows}')
          if shows[0].start_time > datetime.today(): 
            upcomingShowsCount +=1
            upcomingShows.append({
            "venue_id": shows[1].id,
            "venue_name": shows[1].name,
            "venue_image_link": shows[1].image_link,
            "start_time": str(shows[0].start_time)
            })
          else: 
            pastShowsCount +=1
            pastShows.append({
              "venue_id": shows[1].id,
              "venue_name": shows[1].name,
              "venue_image_link": shows[1].image_link,
              "start_time": str(shows[0].start_time)
              
            })
        resultData.append({
          "id": artist.id,
          "name": artist.name,
          "genres": genres,
          "city": artist.city,
          "state": artist.state,
          "phone": artist.phone,
          "facebook_link": artist.facebook_link,
          "seeking_venue": artist.seeking_venue,
          "seeking_description":artist.seeking_description,
          "image_link": artist.image_link,
          "past_shows": pastShows,
          "upcoming_shows": upcomingShows,
          "past_shows_count": pastShowsCount,
          "upcoming_shows_count": upcomingShowsCount, 
        })  
      else:
        resultData.append({
          "id": artist.id,
          "name": artist.name,
          "genres": genres,
          "city": artist.city,
          "state": artist.state,
          "phone": artist.phone,
          "facebook_link": artist.facebook_link,
          "seeking_venue": artist.seeking_venue,
          "seeking_description":artist.seeking_description,
          "image_link": artist.image_link,
          "past_shows": pastShows,
          "upcoming_shows": upcomingShows,
          "past_shows_count": pastShowsCount,
          "upcoming_shows_count": upcomingShowsCount, 
        })  
    data = list(filter(lambda d: d['id'] == artist_id, resultData))[0]
    error=False
  except expression as identifier:
    print(f'{Fore.RED} omg {identifier}')
    flash("Warning: error")
    db.session.rollback()
  finally:
    db.session.close()
    if error: return redirect(url_for('index'))
    else: return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist={
    "id": 4,
    "name": "Guns N Petals",
    "genres": ["Rock n Roll"],
    "city": "San Francisco",
    "state": "CA",
    "phone": "326-123-5000",
    "website": "https://www.gunsnpetalsband.com",
    "facebook_link": "https://www.facebook.com/GunsNPetals",
    "seeking_venue": True,
    "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
    "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80"
  }
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue():
  error=False
  try:
    form = VenueForm(request.form)
    currentVenue = db.session.query(Venue).get(venue_id)
    print(f"{Fore.RED} currentVenue: ", currentVenue)
    genres=''.join(list(filter(lambda x : x!= '{' and x!='}' and x!='"', currentVenue.genres ))).split(',')
    mockVenue={
      "id": 1,
      "name": "The Musical Hop",
      "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
      "address": "1015 Folsom Street",
      "city": "San Francisco",
      "state": "CA",
      "phone": "123-123-1234",
      "website": "https://www.themusicalhop.com",
      "facebook_link": "https://www.facebook.com/TheMusicalHop",
      "seeking_talent": True,
      "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
      "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
    }
    returnedData={
      "id": currentVenue.id,
      "name": currentVenue.name,
      "genres": genres,
      "address": currentVenue.address,
      "city": currentVenue.city,
      "state": currentVenue.state,
      "phone": currentVenue.phone,
      "website": currentVenue.website_link,
      "facebook_link": currentVenue.facebook_link,
      "seeking_talent": currentVenue.seeking_talent,
      "seeking_description": currentVenue.seeking_description,
      "image_link": currentVenue.image_link
    }
  except expression as identifier:
    error=True
    db.rollback()
    print(f'{Fore.Yellow} Error Message: ' , identifier)
    flash('Error when accessing Database: Contact Customer Support if issue persist.')
  finally:
    if error: redirect(url_for('index'))
    else: return render_template('forms/edit_venue.html', form=form, venue=returnedData)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  error=False
  try:
    form = VenueForm(request.form)
    # retrieve the form values
    vName=form.name.data
    vCity=form.city.data.title()
    vState=form.state.data
    vAddress=form.address.data
    vPhone=form.phone.data
    vGenres=form.genres.data
    vWebsite_link = form.website_link.data
    vImage_link=form.image_link.data
    vFacebook_link=form.facebook_link.data
    vSeeking_description=form.seeking_description.data
    #Retrieve BooleanField values and test them. work around hack - BooleanField is buggy
    try:
      #If it can't read it and causes error its not clicked indicating false
      vSeeking_talent= form.seeking_talent.data
    except:
      #set it to false
      vSeeking_talent=False
    finally:
      #if the return value is 'y' or anything else other than a bool then set to true
      if (isinstance(vSeeking_talent, bool) == False):
        vSeeking_talent=True
                
    # TODO: insert form data as a new Venue record in the db, instead
    currentVenueData = db.session.query(Venue).get(venue_id).all()
    currentVenueData.name=vName
    currentVenueData.city=vCity
    currentVenueData.state=vState
    currentVenueData.address=vAddress
    currentVenueData.phone=vPhone
    currentVenueData.genres=vGenrescurrentVenueData
    currentVenueData.image_link=vImage_link
    currentVenueData.facebook_link=vFacebook_link
    currentVenueData.seeking_talent=vSeeking_talent
    currentVenueData.seeking_description=vSeeking_description
    currentVenueData.website_link = vWebsite_link 
    # print('Printing new venue obj: ' ,newVenue , ' || ' ,newVenue.query.all())
    # TODO: modify data to be the data object returned from db insertion
    db.session.add(currentVenueData)
    # on successful db insert, flash success
    db.session.commit()
    flash('Venue ' + vName + ' was successfully listed!')
  except:
    error=True
    db.session.rollback()
    print(sys.exc_info())
    # TODO: on unsuccessful db insert, flash an error instead.
    flash('An error occurred. Venue ' + vName + ' could not be edited.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  finally:
    db.session.close()
    if error: return redirect(url_for('index'))
    else: return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  try:
    form = ArtistForm(request.form)
    # retrieve the form values
    a_Name=form.name.data
    a_City=form.city.data.title()
    a_State=form.state.data
    a_Website_link=form.website_link.data
    a_Phone=form.phone.data
    a_Genres=form.genres.data
    a_Image_link=form.image_link.data
    a_Facebook_link=form.facebook_link.data
    a_Seeking_description=form.seeking_description.data
    print(f'{Fore.YELLOW} omggg')
    print(f'{Fore.YELLOW} Generes1:' , a_Name)  
    
    #Retrieve BooleanField values and test them. work around hack - BooleanField is buggy
    try:
      #If it can't read it and causes error its not clicked indicating false
      a_Seeking_venue= form.seeking_venue.data
    except:
      #set it to false
      a_Seeking_venue=False
    finally:
      #if the return value is 'y' or anything else other than a bool then set to true
      if (isinstance(a_Seeking_venue, bool) == False):
        a_Seeking_venue=True
    # TODO: insert form data as a new Venue record in the db, instead
    print(f'{Fore.YELLOW} sdasfafdas' , a_Seeking_description)
    newArtist = Artist(name=a_Name, city=a_City , state=a_State, website_link=a_Website_link, phone=a_Phone, genres=a_Genres, image_link=a_Image_link, facebook_link=a_Facebook_link,seeking_venue=a_Seeking_venue, seeking_description=a_Seeking_description)
    # print('Printing new venue obj: ' ,newVenue , ' || ' ,newVenue.query.all())
    # TODO: modify data to be the data object returned from db insertion
    db.session.add(newArtist)
    # on successful db insert, flash success
    db.session.commit()
    flash('Artist ' + a_Name + ' was successfully listed!')
  except:
    db.session.rollback()
    print(sys.exc_info())
    # TODO: on unsuccessful db insert, flash an error instead.
    flash('An error occurred. Venue ' + a_Name + ' could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  finally:
    db.session.close()
    return redirect(url_for('index'))


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  try:
    resultData=[]
    mockData=[{
    "venue_id": 1,
    "venue_name": "The Musical Hop",
    "artist_id": 4,
    "artist_name": "Guns N Petals",
    "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
    "start_time": "2019-05-21T21:30:00.000Z"
    }, {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 5,
    "artist_name": "Matt Quevedo",
    "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
    "start_time": "2019-06-15T23:00:00.000Z"
    }, {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 6,
    "artist_name": "The Wild Sax Band",
    "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    "start_time": "2035-04-01T20:00:00.000Z"
    }, {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 6,
    "artist_name": "The Wild Sax Band",
    "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    "start_time": "2035-04-08T20:00:00.000Z"
    }, {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 6,
    "artist_name": "The Wild Sax Band",
    "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    "start_time": "2035-04-15T20:00:00.000Z"
    }]
    showsData = db.session.query(Show, Artist, Venue).filter(Show.artist_id == Artist.id).filter(Venue.id == Show.venue_id).all()
    for shows in showsData:
      if shows[1].deleted and shows[2].deleted:
        shows[0].deleted= True
      if not shows[0].deleted: 
        resultData.append({
        "venue_id": shows[2].id,
        "venue_name": shows[2].name,
        "artist_id": shows[1].id,
        "artist_name": shows[1].name,
        "artist_image_link": shows[1].image_link,
        "start_time": str(shows[0].start_time)
      })
    print(f'{Fore.BLUE} result Data: {resultData}')
  except expression as identifier:
    db.session.rollback()
    print(identifier)
    flash('An error occurred.')
  finally:
    return render_template('pages/shows.html', shows=resultData)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST']) #create datatable
def create_show_submission():
  error = True
  try:
    date_format = '%Y-%m-%d %H:%M:%S'
    show = Show()
    form = ShowForm(request.form)
    artistID =form.artist_id.data
    venueID=form.venue_id.data
    startDate = form.start_time.data
    venue = Venue.query.get(venueID)
    artist = Artist.query.get(artistID)
    if (venue and artist) and not (venue.deleted and artist.deleted):
      if (venue.seeking_talent and artist.seeking_venue ):
        show.artist_id = artistID
        show.venue_id = venueID
        show.start_time = datetime.strptime(startDate, date_format)
        venue.num_of_shows +=1
        artist.num_of_shows +=1
        db.session.add(show) 
        db.session.commit()
        error = False
        flash('Show was successfully listed!')
      else:
        if not artist.seeking_venue: 
          flash( artist.name + ' is not seeking a venue - Artist ID: ' + artistID)
        if ( not venue.seeking_talent):
          flash(venue.name+ ' is not seeking talent - Venue ID: '+ venueID )
    else:
      if not (artist or artist.deleted):
        flash('Invalid Artist Id !')
      if not (venue or venue.deleted):
        flash('Invalid Venue Id !')
  except Exception as e:
    print(f'{Fore.RED}Error ==> {e}')
    db.session.rollback()
  finally:
    db.session.close()
    if error:
      return redirect(url_for('create_shows')) 
    else:
      return redirect(url_for('index')) 

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#


# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
