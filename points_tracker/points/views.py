from rest_framework.response import Response
from .models import Transaction
from rest_framework import status
from rest_framework.views import APIView
from django.db.models import Sum
import json
from django.utils.dateparse import parse_datetime

"""
This view is used to add points. It takes in the payer name,
points to add, and timestamp as a string in the format "YYYY-MM-DDTHH:MM:SSZ".
If the points value is negative, it will invoke the spend logic.
"""
class AddPointsView(APIView):
    def post(self, request):
        # Get data from request
        data = json.loads(request.body)
        payer = data.get('payer')
        points = data.get('points')
        timestamp_str = data.get('timestamp')

        # Parse timestamp string into datetime object
        timestamp = parse_datetime(timestamp_str)

        # Validate input
        if payer and points is not None and timestamp:
            # If points are negative, invoke the spend logic
            if points < 0:
                result = spend_points(abs(points))

                # If there is an error, return it
                if 'error' in result:
                    return Response({'error': result['error']}, status=400)
            else:
                # Save the transaction if not a negative transaction or spend was successful
                transaction = Transaction(payer=payer, points=points, timestamp=timestamp)
                transaction.save()
            return Response({}, status=status.HTTP_200_OK)

        # If any of the required fields are missing, return an error
        return Response({'error': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)


"""
This view is used to spend points. It takes in the points to spend, invokes the spend logic, and returns the spent points.
"""
class SpendPointsView(APIView):
    def post(self, request):
        points_to_spend = request.data.get('points')

        # Validate input
        if points_to_spend is None or points_to_spend <= 0:
            return Response("Invalid number of points", status=status.HTTP_400_BAD_REQUEST)

        # Invoke the spend logic
        result = spend_points(points_to_spend)

        # If there is an error, return it
        if 'error' in result:
            return Response(result['error'], status=status.HTTP_400_BAD_REQUEST)

        return Response(result, status=status.HTTP_200_OK)


"""
This view is used to get the remaining balance at any given time. It returns a dictionary with the balance of each payer.
"""
class PointsBalanceView(APIView):
    def get(self, request):
        # Get balance
        balance = Transaction.objects.values('payer').annotate(points=Sum('points')).order_by()
        balance_dict = {entry['payer']: entry['points'] for entry in balance}
        return Response(balance_dict, status=status.HTTP_200_OK)

"""
    This function handles the spending logic for the spend points endpoint.
    
    :param points_to_spend: The number of points to spend.
    :return: A list of dictionaries of the form {"payer": string, "points": int},
             or {"error": string} if there was an error.
    """
def spend_points(points_to_spend):
    # Get total points
    total_points = Transaction.objects.aggregate(total=Sum('points'))['total']

    # If total points is None, set it to 0
    if total_points is None:
        total_points = 0

    # If total points is less than points to spend, return an error
    if total_points < points_to_spend:
        return {"error": "Not enough points"}

    # Initialize variables
    transactions = Transaction.objects.all().order_by('timestamp')
    spent_points = []
    remaining_points = points_to_spend

    # Fetch all transactions, ordered by timestamp (oldest first)
    for transaction in transactions:

        # Calculate how many points can be spent from that transaction
        if remaining_points <= 0:
            break
        
        if transaction.points > 0:
            # Calculate how many points can be spent
            spend = min(transaction.points, remaining_points)
            remaining_points -= spend
            spent_points.append({"payer": transaction.payer, "points": -spend})

            # Update transaction points
            transaction.points -= spend
            transaction.save()

    return spent_points
