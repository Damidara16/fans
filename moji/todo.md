updates to push after online

middleware:
1. when blocked but still in following, user can view content but cant like or comment

webhooks:
1. to remove user from following
2. keep user in following until subscription ends

view edits:
1. add a if a user has a confirmed card to payment views

notes:
1. set up emails stripe, etc in settings


bundle
celeb creates a plan and sends a requests to other user to create bundle model
model gets both plans and creates a sperate billing cycles with two customer models
coupons can not be used on bundle models
when the user wants to end, the view will go to the bundle model and end both plans
