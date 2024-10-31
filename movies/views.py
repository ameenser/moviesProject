from django.shortcuts import render , HttpResponse,redirect
from .models import Movie, Comment
from .forms import CommentForm
# Create your views here.
def movie_list(request) :
    movies = Movie.objects.all().order_by('date')
    return render (request,'movie_list.html', {'movies': movies})

def movie_detail(request,slug):
    # return HttpResponse(slug)
    movie = Movie.objects.get(slug = slug)
    comments = movie.comments.all()
    
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.movie = movie
                comment.user = request.user
                comment.save()
                return redirect('movies:detail', slug=slug)  # Redirect after post
        else:
            return redirect('accounts:login')
    else:
        form = CommentForm()

    return render(request, 'movie_detail.html', {
        'movie': movie,
        'comments': comments,
        'form': form,
    })