from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Auction(models.Model):
	name = models.CharField(max_length=35)
	owner = models.ForeignKey(User, on_delete=models.CASCADE)
	description = models.CharField(max_length=350)
	category = models.CharField(max_length=35)
	picture = models.URLField(max_length=200)
	creationdate = models.DateTimeField()
	price = models.IntegerField(default=0)
	isactive = models.BooleanField(default=True)

	def __str__(self):
   		return self.name + " - SOLD BY: " + str(self.owner)


class Bids(models.Model):
	id_auction = models.ForeignKey('Auction', on_delete=models.CASCADE)
	current_bid = models.IntegerField()
	current_winner = models.ForeignKey('User', on_delete=models.CASCADE)
	date_bid = models.DateTimeField()

	def __str__(self):
   		return str(self.current_winner) + " - " + str(self.current_bid) + "$ - DATE : " + str(self.date_bid) + " - ON : " + str(self.id_auction)

class Comment(models.Model):
	id_auction = models.ForeignKey('Auction', on_delete=models.CASCADE)
	comment = models.CharField(max_length=350)
	comment_date = models.DateTimeField()
	id_sender = models.ForeignKey('User', on_delete=models.CASCADE)

	def __str__(self):
   		return str(self.id_sender) + " - ON DATE: " + str(self.comment_date) + " - " + str(self.comment) + " - ON : " + str(self.id_auction)

class Watchlist(models.Model):
	id_user = models.ForeignKey('User', on_delete=models.CASCADE)
	id_auction = models.ForeignKey('Auction', on_delete=models.CASCADE)

	def __str__(self):
   		return self.id

	
		





