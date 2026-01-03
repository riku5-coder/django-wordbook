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
    誰でもアクセス可能
    機能説明と導線を表示
    """
    return render(request, "core/top.html")



def word_search(request):
    query = request.GET.get("q")
    meanings = [] # meaningsはリスト
    error = None

    if query:
        try:
            # loolup_enja(utils.pyにある)は文字列のリストを返す。インデックス0が主要な意味。
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

# apiで検索した単語を登録する。フォームを使うとかえって煩雑になるのでフォームは使わない
@login_required
def register_word(request):
    if request.method == "POST":
        word = request.POST.get("word", "").strip()
        meaning_list = request.POST.getlist("meaning")

        # 空文字を除去
        meaning_list = [m.strip() for m in meaning_list if m.strip()]

        if not meaning_list:
            return HttpResponseBadRequest("meaning is required")

        if len(meaning_list) == 1:
            meaning = meaning_list[0]
        else:
            # 自動で全部の意味を登録した場合、1. 意味 2. 意味　3. 意味…　のような形で登録
            meaning = "  ".join(
                f"{i + 1}. {m}" for i, m in enumerate(meaning_list)
            )

        UserWord.objects.create(
            user=request.user,
            word=word,
            meaning=meaning,
            source="excelapi"
        )

        return redirect("word_search")


# 登録した単語のリストを表示する。
# ログインしていればそのユーザーのリスト、そうでなければ登録されたすべての単語リスト。
# 
def word_list(request):
    period = request.GET.get("period")
    now = timezone.now()
        # ベースとなる QuerySet を決める
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

    # 本人チェック
    if word.user != request.user:
        raise PermissionDenied
    # フォームを使って編集された単語を登録する
    if request.method == "POST":
        form = WordCreateForm(request.POST, instance=word)
        if form.is_valid():
            form.save()
            return redirect("word_list")
    
    else:
        form = WordCreateForm(instance=word)

    return render(
        request,
        "core/word_edit.html",
        {
            "form": form,
            "word_obj": word, #削除url用
        }
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


#フラッシュカードは今日、直近一週間、直近一か月でソートする
@login_required
def flashcards(request):
    period = request.GET.get("period", "today")

    now = timezone.now()

    qs = UserWord.objects.filter(user=request.user)

    if period == "today":
        start = now.date()
        qs = qs.filter(created_at__date=start)

    #一週間以内のものを取得
    elif period == "week":
        start = now - timedelta(days=7)
        qs = qs.filter(created_at__gte=start)
    #一か月いないのものを取得
    elif period == "month":
        start = now - timedelta(days=30)
        qs = qs.filter(created_at__gte=start)

    elif period == "all":
        pass  # すべてなので絞り込みはなし

    qs = qs.order_by("-created_at")[:50]

    return render(request, "core/flashcards.html", {
        "words": qs,
        "period": period,
    })