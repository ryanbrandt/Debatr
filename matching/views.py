from django.shortcuts import render
import gensim

def matching(request):
    user = request.user
    model = gensim.models.word2vec.Word2Vec.load('matching/match_model')
    print(model.similarity('donald', 'donald'))
    return render(request, 'matching.html', {})
