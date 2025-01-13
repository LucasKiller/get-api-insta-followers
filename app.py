from flask import Flask, redirect, request, jsonify
import requests

app = Flask(__name__)

# Configurações do Instagram
CLIENT_ID = "1192672039076047"
CLIENT_SECRET = "13988311217058edd577fc254e8244ae"
REDIRECT_URI = "https://get-api-insta-followers.onrender.com/callback"


@app.route('/')
def home():
    """Redireciona diretamente para o autenticador do Instagram"""
    auth_url = (
        f"https://www.instagram.com/oauth/authorize?"
        f"enable_fb_login=0&force_authentication=1"
        f"&client_id={CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&response_type=code"
        f"&scope=instagram_business_basic%2Cinstagram_business_manage_messages%2Cinstagram_business_manage_comments%2Cinstagram_business_content_publish"
    )
    return redirect(auth_url)


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
    profile_url = f"https://graph.instagram.com/v21.0/me?fields=id,username,account_type,media_count,followers_count&access_token={access_token}"
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
        # Renderizar formulário para quem tem menos de 100k seguidores
        return """
            <html>
            <head><title>Formulário de Cadastro</title></head>
            <body>
                <div class="form-container">
                    <form id="instagramForm">
                        <input type="text" name="nome" placeholder="Nome">
                        <input type="email" name="email" placeholder="E-mail">
                        <input type="text" name="cidade" placeholder="Cidade">
                        <input type="text" name="instagram" id="instagramUsername" placeholder="@ do Instagram" required>
                        <select name="seguidores">
                            <option value="" disabled selected>Nº de Seguidores</option>
                            <option value="menos-1000">Menos de 1.000</option>
                            <option value="1000-5000">1.000 - 5.000</option>
                            <option value="5000-10000">5.000 - 10.000</option>
                            <option value="mais-10000">Mais de 10.000</option>
                        </select>
                        <button type="submit">Enviar</button>
                    </form>
                </div>
                <style>
                    .form-container {{
                        background-color: #1B263B;
                        padding: 20px;
                        border-radius: 8px;
                        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
                        width: 100%;
                        max-width: 400px;
                        margin: 0 auto;
                    }}
                    .form-container input, 
                    .form-container select, 
                    .form-container button {{
                        width: 100%;
                        padding: 10px;
                        margin-bottom: 15px;
                        border: 1px solid #415A77;
                        border-radius: 4px;
                        background-color: #1B263B;
                        color: #E0E1DD;
                        font-size: 14px;
                    }}
                    .form-container button {{
                        background-color: #38E5E7;
                        color: #0D1B2A;
                        font-weight: bold;
                        cursor: pointer;
                        border: none;
                        transition: background-color 0.3s;
                    }}
                    .form-container button:hover {{
                        background-color: #2DC1C2;
                    }}
                    .form-container input::placeholder {{
                        color: #7D8895;
                    }}
                </style>
            </body>
            </html>
        """


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
