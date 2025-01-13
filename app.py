from flask import Flask, request, redirect, jsonify
import requests

app = Flask(__name__)

# Configurações do Instagram
CLIENT_ID = "1192672039076047"
CLIENT_SECRET = "13988311217058edd577fc254e8244ae"
REDIRECT_URI = "https://get-api-insta-followers.onrender.com/callback"  # Atualize com seu domínio do Render


@app.route('/')
def home():
    """Rota inicial para exibir o botão de login"""
    auth_url = (
        f"https://www.instagram.com/oauth/authorize?"
        f"client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code&scope=instagram_business_basic"
    )
    return f"""
        <html>
        <head><title>Login com Instagram</title></head>
        <body>
            <button onclick="window.open('{auth_url}', '_blank', 'width=500,height=700')">
                Login com Instagram
            </button>
        </body>
        </html>
    """


@app.route('/callback')
def callback():
    """Rota para processar o código retornado pelo Instagram"""
    code = request.args.get('code')
    if not code:
        return jsonify({"error": "Nenhum código retornado pelo Instagram."}), 400

    # Trocar o código pelo token de acesso
    token_url = "https://api.instagram.com/oauth/access_token"
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "authorization_code",
        "redirect_uri": REDIRECT_URI,
        "code": code,
    }
    response = requests.post(token_url, data=data)
    if response.status_code != 200:
        return jsonify({"error": "Erro ao obter o token de acesso.", "details": response.json()}), 400

    access_token = response.json().get("access_token")
    user_id = response.json().get("user_id")

    # Obter informações do perfil
    profile_url = f"https://graph.instagram.com/{user_id}?fields=id,username,account_type,media_count,followers_count&access_token={access_token}"
    profile_response = requests.get(profile_url)

    if profile_response.status_code != 200:
        return jsonify({"error": "Erro ao obter informações do perfil.", "details": profile_response.json()}), 400

    profile_data = profile_response.json()
    followers = profile_data.get("followers_count", 0)

    # Redirecionar com base no número de seguidores
    if followers > 5000000:
        return redirect("https://exercitodeinfluencia.com.br/5mm/")
    elif followers > 1000000:
        return redirect("https://exercitodeinfluencia.com.br/1mm-a-5mm/")
    elif followers > 500000:
        return redirect("https://exercitodeinfluencia.com.br/500k-a-1mm/")
    elif followers > 100000:
        return redirect("https://exercitodeinfluencia.com.br/100k-a-500k/")
    else:
        return jsonify({"error": "A conta precisa ter pelo menos 100k seguidores."}), 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
