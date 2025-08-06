from django.shortcuts import render
import json
from django.http import JsonResponse
from .models import Book
from django.core.exceptions import ObjectDoesNotExist
from datetime import date, datetime
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

@csrf_exempt
def book_list(request):
        if request.method == "GET":
            books = Book.objects.all()

            data = []
            for book in books:
                data.append({
                    'id':book.id,
                    'author':book.author, 
                    'title':book.title,
                    'isbn': book.isbn,
                    'publishedDate': book.publishedDate,
                })
            
            return JsonResponse(data, safe=False)

        elif request.method == "POST":
            try:
                data = json.loads(request.body)
                title = data.get('title')
                author = data.get('author')
                isbn = data.get('isbn')
                price = data.get('price')
                published_date_str = data.get('publishedDate')

                if not all([title, author, isbn, price, published_date_str]):
                    return JsonResponse({"error": 'Missing required fields title, author, isbn, price, publishedDate'}, status = 400)

                try:
                    published_date = datetime.strptime(published_date_str, '%Y-%m-%d').date()
                except ValueError:
                    return JsonResponse({'error': 'Invalid publishedDate format. Use YYYY-MM-DD'}, status=400)

                # if Book.objects.filter(isbn = isbn):
                #     return JsonResponse({'error': f'Book with ISBN {isbn} already exists.'}, status=409)

                book = Book.objects.create(
                    title = title,
                    author = author,
                    price = price,
                    isbn = isbn,
                    publishedDate = published_date
                )

                return JsonResponse({
                'id': book.id,
                'title': book.title,
                'author': book.author,
                'price': float(book.price),
                'isbn': book.isbn,
                'publishedDate': book.publishedDate.isoformat()
            }, status=201)

            except json.JSONDecodeError:
                return JsonResponse({'error': 'Invalid JSON in request body'}, status=400)
            except Exception as e:
            # Catch any other unexpected errors
                return JsonResponse({'error': str(e)}, status=500)

        return JsonResponse({"error":"Method not allowed"}, status = 405)

@csrf_exempt
def book_detail(request,pk):
    try:
        book = Book.objects.get(pk = pk)
    except ObjectDoesNotExist:
        return JsonResponse({"error":"Book not found"}, status=404)
    if request.method == "GET":
        return JsonResponse({
            'id':book.id,
            'author':book.author,
            'price':book.price,
            'isbn':book.isbn,
            'publishedDate':book.publishedDate.isoformat()

        })

    elif request.method == "PUT":
        try:
            data = json.loads(request.body)

            if 'title' in data:
                book.title = data['title']
            
            if 'author' in data:
                book.author = data['author']
            
            if 'price' in data:
                book.price = data['price']

            if 'isbn' in data:
                # we can also check here for uniqueness of the isbn number.
                book.isbn = data['isbn']

            if 'publishedDate' in data:
                try:
                    book.publishedDate = datetime.strptime(data['publishedDate'], '%Y-%m-%d').date()
                except ValueError:
                    return JsonResponse({"error":"Invalid Published Date format Y-M-D"}, status=400)

                
            book.save()


            return JsonResponse({
                'id': book.id,
                'title': book.title,
                'author': book.author,
                'price': float(book.price),
                'isbn': book.isbn,
                'publishedDate': book.publishedDate.isoformat()
            })


        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON in request body'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    elif request.method == "DELETE":

        book.delete()

        return JsonResponse({'message': 'Book deleted successfully'}, status=204)

    return JsonResponse({'error': 'Method Not Allowed'}, status=405)

            
