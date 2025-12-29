from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponseBadRequest
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .utils import lookup_enja
from .models import UserWord
from .forms import WordCreateForm
from django.utils import timezone
from datetime import timedelta
# Create your views here.

def top(request):
    """
    トップページ
    ・誰でもアクセス可能
    ・機能説明と導線を表示
    """
    return render(request, "core/top.html")



def word_search(request):
    query = request.GET.get("q")
    meanings = [] # meaningsはリスト
    error = None

    if query:
        try:
            # loolup_enjaは文字列のリストを返す。インデックス0が主要な意味。
            meanings = lookup_enja(query)
        except Exception:
            error = "辞書の検索に失敗しました"

    return render(
        request,
        "core/search.html",
        {
            "query": query,
            "meanings": meanings,
            "error": error,
        }
    )

# apiで検索した単語を登録する
@login_required
def register_word(request):
    if request.method == "POST":
        word = request.POST.get("word")
        meaning_list = request.POST.getlist("meaning")
        
        if not meaning_list:
            return HttpResponseBadRequest("meaning is required")

        if len(meaning_list) == 1:
            meaning = meaning_list[0]
        
        elif len(meaning_list) >= 2:
            for i in range(len(meaning_list)):
                meaning_list[i] = str(i + 1) + '. ' + meaning_list[i]
            # 半角スペース２つでつないで文字列にする
            meaning = '  '.join(meaning_list)


        UserWord.objects.create(
            user=request.user,
            word=word,
            meaning=meaning,
            source="excelapi"
        )

    return redirect("word_search")




def word_list(request):
    period = request.GET.get("period")
    now = timezone.now()
        # --- ① ベースとなる QuerySet を決める ---
    if request.user.is_authenticated:
        # ログイン中：自分の単語のみ
        qs = UserWord.objects.filter(user=request.user)
        is_public = False
    else:
        # 未ログイン：全ユーザーの単語
        qs = UserWord.objects.all()
        is_public = True


    if period == "today":
        qs = qs.filter(created_at__date=now.date())
    elif period == "week":
        qs = qs.filter(created_at__gte=now - timedelta(days=7))
    elif period == "month":
        qs = qs.filter(created_at__gte=now - timedelta(days=30))


    qs = qs.order_by("-created_at")

    return render(request, "core/word_list.html", {
        "words": qs,
        "period": period,
        "is_public": is_public,
    })


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # 登録後すぐログイン
            return redirect("top")
    else:
        form = UserCreationForm()

    return render(request, "core/signup.html", {"form": form})


@login_required
def word_edit(request, pk):
    word = get_object_or_404(UserWord, pk=pk)

    # 本人チェック（超重要）
    if word.user != request.user:
        raise PermissionDenied

    if request.method == "POST":
        word.word = request.POST.get("word", "").strip()
        word.meaning = request.POST.get("meaning", "").strip()
        word.save()
        return redirect("word_list")

    return render(
        request,
        "core/word_edit.html",
        {"word_obj": word}
    )

@login_required
def word_delete(request, pk):
    word = get_object_or_404(UserWord, pk=pk)

    if word.user != request.user:
        raise PermissionDenied

    if request.method == "POST":
        word.delete()
        return redirect("word_list")

    return redirect("word_edit", pk=pk)


@login_required
def word_create(request):
    if request.method == "POST":
        form = WordCreateForm(request.POST)
        if form.is_valid():
            word = form.save(commit=False)
            word.user = request.user
            word.source = 'manual'
            word.save()
            return redirect("word_list")
    else:
        form = WordCreateForm()

    return render(request, "core/word_create.html", {
        "form": form
    })

