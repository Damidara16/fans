future updates:

1. In product models, add points feature recurring subscriptions and track shares that lead to subscriptions
2. make a middleware the brute force url action, like delete, block, access so so.
3. add a spotlight to user profiles that shows there most loyal fans of the week, this an optional feature
4. add a transction history to users for payouts, payments, etc
5. add pointsWallet to user profile
6. add account views
7. have a middleware that blocks people from making another connect account if they already have
8. add analytics


NOTES:
add a report and strike system

i need a way to track points that are spent, so that a user cant just spend and relike content to get the points back.

add view to add user content to user preview, and remove from preview


send notification for views

list of user notifications
add a notification model to user for setting settings
(O) = optional
------------
new subscriptions (O)
re-new subscriptions (O)
Like (O)
Comment (O)
account created
login with location and time
reward redeemed
points add (O)
points spent (O)
bank info changed
strike against account
tips/transactions (O)
monthly summary
payout sent


sub -> take celeb id and request user, send data to view and goes on from their
tip -> take celeb, request user id and amount and message send data to view and goes on from their
cancel -> send data to view and goes on from their
report -> send data to view and goes on from their


all thats left to do is add the notification to views if needed, add a ui, add security for some view holes
