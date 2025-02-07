from flask import Flask, jsonify, request
import yfinance as yf
from flask_cors import CORS

# ✅ Flask 앱 객체 생성
app = Flask(__name__)
CORS(app)  # CORS 설정 추가 (프론트엔드 연동)

def format_stock_code(stock_code):
    """ 한국 주식이면 .KS를 붙이고, 해외 주식이면 그대로 반환 """
    stock_code = stock_code.strip().replace('\n', '').replace('%0A', '').replace('\r', '')  # ✅ 개행 문자 완전 제거
    if stock_code.isdigit():  # 종목 코드가 숫자로만 되어 있다면 한국 주식
        return f"{stock_code}.KS"  # KOSPI 종목 코드
    return stock_code  # 해외 주식은 그대로 사용

def get_stock_info(stock_code):
    """ Yahoo Finance API를 이용하여 주식 기본 정보를 가져오기 """
    try:
        formatted_code = format_stock_code(stock_code)
        stock = yf.Ticker(formatted_code)
        info = stock.info

        if not info or 'currentPrice' not in info:
            return {"error": "Yahoo Finance에서 데이터를 가져오지 못했습니다."}

        stock_data = {
            "stock_code": stock_code,
            "company_name": info.get("longName"),
            "market_cap": info.get("marketCap"),
            "current_price": info.get("currentPrice"),
            "52_week_high": info.get("fiftyTwoWeekHigh"),
            "52_week_low": info.get("fiftyTwoWeekLow"),
            "sector": info.get("sector"),
            "industry": info.get("industry"),
        }
        return stock_data
    except Exception as e:
        return {"error": f"데이터를 가져오는 중 오류 발생: {str(e)}"}

@app.route('/stock_info', methods=['GET'])
def stock_info():
    """ 주식 기본 정보 조회 API - Query Parameter 방식 지원 """
    stock_code = request.args.get("stock_code", "").strip().replace('\n', '').replace('%0A', '').replace('\r', '')  # ✅ 개행 문자 완전 제거

    # ✅ 요청된 종목 코드 출력 (로그 확인용)
    print(f"📌 Received stock_code: '{stock_code}'")

    if not stock_code:
        return jsonify({"error": "stock_code 파라미터가 필요합니다."}), 400

    data = get_stock_info(stock_code)
    return jsonify(data)

def get_financials(stock_code):
    """ Yahoo Finance에서 재무제표 데이터를 가져오기 """
    try:
        formatted_code = format_stock_code(stock_code)
        stock = yf.Ticker(formatted_code)

        balance_sheet = stock.balance_sheet
        income_statement = stock.financials
        cash_flow = stock.cashflow

        # ✅ 데이터가 없으면 에러 반환
        if balance_sheet.empty or income_statement.empty or cash_flow.empty:
            return {"error": "Yahoo Finance에서 제공하는 재무제표 데이터가 없습니다."}

        # ✅ Timestamp 인덱스 제거 & 문자열 변환
        balance_sheet = balance_sheet.reset_index()
        income_statement = income_statement.reset_index()
        cash_flow = cash_flow.reset_index()

        balance_sheet.columns = balance_sheet.columns.astype(str)
        income_statement.columns = income_statement.columns.astype(str)
        cash_flow.columns = cash_flow.columns.astype(str)

        # ✅ JSON 변환 (index 없이 records 형태)
        financials = {
            "balance_sheet": balance_sheet.to_dict(orient="records"),
            "income_statement": income_statement.to_dict(orient="records"),
            "cash_flow": cash_flow.to_dict(orient="records")
        }

        return financials
    except Exception as e:
        return {"error": f"재무제표 데이터를 가져오는 중 오류 발생: {str(e)}"}

@app.route('/financials', methods=['GET'])
def financials():
    """ 주식 재무제표 조회 API - Query Parameter 방식 지원 """
    stock_code = request.args.get("stock_code", "").strip().replace('\n', '').replace('%0A', '').replace('\r', '')  # ✅ 개행 문자 완전 제거

    if not stock_code:
        return jsonify({"error": "stock_code 파라미터가 필요합니다."}), 400

    data = get_financials(stock_code)
    return jsonify(data)

def get_chart_data(stock_code):
    """ Yahoo Finance에서 최근 6개월간 주가 데이터를 가져오기 """
    try:
        formatted_code = format_stock_code(stock_code)
        stock = yf.Ticker(formatted_code)
        hist = stock.history(period="6mo")  # 최근 6개월간 데이터 가져오기
        dates = hist.index.strftime("%Y-%m-%d").tolist()
        prices = hist["Close"].tolist()

        if not dates or not prices:
            return {"error": "차트 데이터를 가져올 수 없습니다."}

        return {"dates": dates, "prices": prices}
    except Exception as e:
        return {"error": f"차트 데이터를 가져오는 중 오류 발생: {str(e)}"}

@app.route('/chart_data', methods=['GET'])
def chart_data():
    """ 주가 차트 데이터 제공 API - Query Parameter 방식 지원 """
    stock_code = request.args.get("stock_code", "").strip().replace('\n', '').replace('%0A', '').replace('\r', '')  # ✅ 개행 문자 완전 제거

    if not stock_code:
        return jsonify({"error": "stock_code 파라미터가 필요합니다."}), 400

    data = get_chart_data(stock_code)
    return jsonify(data)

if __name__ == '__main__':
    # ✅ Flask에서 등록된 엔드포인트 출력 (디버깅용)
    print("\n📌 Registered Routes:")
    for rule in app.url_map.iter_rules():
        print(f"🔹 {rule}")

    app.run(debug=False)  # ✅ debug=False 설정으로 요청 차이 줄이기


























