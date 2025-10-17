2025-10-17T22:08:39.384173819Z [inf]  Requirement already satisfied: cryptography>=2.6.1 in /usr/local/lib/python3.11/site-packages (from ccxt>=4.0.0->-r requirements.txt (line 10)) (46.0.3)
2025-10-17T22:08:39.387269619Z [inf]  Requirement already satisfied: aiohttp>=3.10.11 in /usr/local/lib/python3.11/site-packages (from ccxt>=4.0.0->-r requirements.txt (line 10)) (3.13.1)
2025-10-17T22:08:39.387277322Z [inf]  Requirement already satisfied: aiodns>=1.1.1 in /usr/local/lib/python3.11/site-packages (from ccxt>=4.0.0->-r requirements.txt (line 10)) (3.5.0)
2025-10-17T22:08:39.390048792Z [inf]  Requirement already satisfied: yarl>=1.7.2 in /usr/local/lib/python3.11/site-packages (from ccxt>=4.0.0->-r requirements.txt (line 10)) (1.22.0)
2025-10-17T22:08:39.400756590Z [inf]  Requirement already satisfied: pycares>=4.9.0 in /usr/local/lib/python3.11/site-packages (from aiodns>=1.1.1->ccxt>=4.0.0->-r requirements.txt (line 10)) (4.11.0)
2025-10-17T22:08:39.411523394Z [inf]  Requirement already satisfied: aiohappyeyeballs>=2.5.0 in /usr/local/lib/python3.11/site-packages (from aiohttp>=3.10.11->ccxt>=4.0.0->-r requirements.txt (line 10)) (2.6.1)
2025-10-17T22:08:39.411539972Z [inf]  Requirement already satisfied: aiosignal>=1.4.0 in /usr/local/lib/python3.11/site-packages (from aiohttp>=3.10.11->ccxt>=4.0.0->-r requirements.txt (line 10)) (1.4.0)
2025-10-17T22:08:39.415502718Z [inf]  Requirement already satisfied: attrs>=17.3.0 in /usr/local/lib/python3.11/site-packages (from aiohttp>=3.10.11->ccxt>=4.0.0->-r requirements.txt (line 10)) (25.4.0)
2025-10-17T22:08:39.415512070Z [inf]  Requirement already satisfied: frozenlist>=1.1.1 in /usr/local/lib/python3.11/site-packages (from aiohttp>=3.10.11->ccxt>=4.0.0->-r requirements.txt (line 10)) (1.8.0)
2025-10-17T22:08:39.415519943Z [inf]  Requirement already satisfied: multidict<7.0,>=4.5 in /usr/local/lib/python3.11/site-packages (from aiohttp>=3.10.11->ccxt>=4.0.0->-r requirements.txt (line 10)) (6.7.0)
2025-10-17T22:08:39.420219928Z [inf]  Requirement already satisfied: propcache>=0.2.0 in /usr/local/lib/python3.11/site-packages (from aiohttp>=3.10.11->ccxt>=4.0.0->-r requirements.txt (line 10)) (0.4.1)
2025-10-17T22:08:39.487615684Z [inf]  Requirement already satisfied: cffi>=2.0.0 in /usr/local/lib/python3.11/site-packages (from cryptography>=2.6.1->ccxt>=4.0.0->-r requirements.txt (line 10)) (2.0.0)
2025-10-17T22:08:39.510639188Z [inf]  Requirement already satisfied: anyio in /usr/local/lib/python3.11/site-packages (from httpx<0.29,>=0.26->supabase>=2.0.0->-r requirements.txt (line 6)) (4.11.0)
2025-10-17T22:08:39.510646448Z [inf]  Requirement already satisfied: httpcore==1.* in /usr/local/lib/python3.11/site-packages (from httpx<0.29,>=0.26->supabase>=2.0.0->-r requirements.txt (line 6)) (1.0.9)
2025-10-17T22:08:39.540849911Z [inf]  Requirement already satisfied: annotated-types>=0.6.0 in /usr/local/lib/python3.11/site-packages (from pydantic!=1.8,!=1.8.1,!=2.0.0,!=2.0.1,!=2.1.0,<3.0.0,>=1.7.4->fastapi==0.108.0->-r requirements.txt (line 2)) (0.7.0)
2025-10-17T22:08:39.545513613Z [inf]  Requirement already satisfied: pydantic-core==2.41.4 in /usr/local/lib/python3.11/site-packages (from pydantic!=1.8,!=1.8.1,!=2.0.0,!=2.0.1,!=2.1.0,<3.0.0,>=1.7.4->fastapi==0.108.0->-r requirements.txt (line 2)) (2.41.4)
2025-10-17T22:08:39.545529995Z [inf]  Requirement already satisfied: typing-inspection>=0.4.2 in /usr/local/lib/python3.11/site-packages (from pydantic!=1.8,!=1.8.1,!=2.0.0,!=2.0.1,!=2.1.0,<3.0.0,>=1.7.4->fastapi==0.108.0->-r requirements.txt (line 2)) (0.4.2)
2025-10-17T22:08:39.562763945Z [inf]  Requirement already satisfied: six>=1.5 in /usr/local/lib/python3.11/site-packages (from python-dateutil>=2.8.2->pandas==2.0.3->-r requirements.txt (line 4)) (1.17.0)
2025-10-17T22:08:40.228836514Z [inf]  Requirement already satisfied: h2<5,>=3 in /usr/local/lib/python3.11/site-packages (from httpx[http2]<0.29,>=0.26->postgrest->supabase>=2.0.0->-r requirements.txt (line 6)) (4.3.0)
2025-10-17T22:08:40.228848673Z [inf]  Requirement already satisfied: hyperframe<7,>=6.1 in /usr/local/lib/python3.11/site-packages (from h2<5,>=3->httpx[http2]<0.29,>=0.26->postgrest->supabase>=2.0.0->-r requirements.txt (line 6)) (6.1.0)
2025-10-17T22:08:40.228856114Z [inf]  Requirement already satisfied: hpack<5,>=4.1 in /usr/local/lib/python3.11/site-packages (from h2<5,>=3->httpx[http2]<0.29,>=0.26->postgrest->supabase>=2.0.0->-r requirements.txt (line 6)) (4.1.0)
2025-10-17T22:08:40.228862536Z [err]  WARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager. It is recommended to use a virtual environment instead: https://pip.pypa.io/warnings/venv
2025-10-17T22:08:40.228894020Z [inf]  Requirement already satisfied: sniffio>=1.1 in /usr/local/lib/python3.11/site-packages (from anyio->httpx<0.29,>=0.26->supabase>=2.0.0->-r requirements.txt (line 6)) (1.3.1)
2025-10-17T22:08:40.228896009Z [inf]  Requirement already satisfied: deprecation>=2.1.0 in /usr/local/lib/python3.11/site-packages (from postgrest->supabase>=2.0.0->-r requirements.txt (line 6)) (2.1.0)
2025-10-17T22:08:40.228905788Z [inf]  Requirement already satisfied: pyjwt>=2.10.1 in /usr/local/lib/python3.11/site-packages (from pyjwt[crypto]>=2.10.1->supabase-auth->supabase>=2.0.0->-r requirements.txt (line 6)) (2.10.1)
2025-10-17T22:08:40.228907960Z [inf]  Requirement already satisfied: pycparser in /usr/local/lib/python3.11/site-packages (from cffi>=2.0.0->cryptography>=2.6.1->ccxt>=4.0.0->-r requirements.txt (line 10)) (2.23)
2025-10-17T22:08:40.228913542Z [inf]  Requirement already satisfied: strenum>=0.4.15 in /usr/local/lib/python3.11/site-packages (from supabase-functions->supabase>=2.0.0->-r requirements.txt (line 6)) (0.4.15)
2025-10-17T22:08:40.228918658Z [inf]  Requirement already satisfied: packaging in /usr/local/lib/python3.11/site-packages (from deprecation>=2.1.0->postgrest->supabase>=2.0.0->-r requirements.txt (line 6)) (25.0)
2025-10-17T22:08:40.325080347Z [err]  
2025-10-17T22:08:40.325091073Z [err]  [notice] A new release of pip is available: 24.0 -> 25.2
2025-10-17T22:08:40.325098026Z [err]  [notice] To update, run: pip install --upgrade pip
2025-10-17T22:08:40.520678178Z [inf]  Starting FastAPI with uvicorn...
2025-10-17T22:08:42.246013205Z [inf]  ✅ Supabase connection established
2025-10-17T22:08:42.246023002Z [err]  INFO:     Started server process [10]
2025-10-17T22:08:42.246032979Z [err]  INFO:     Waiting for application startup.
2025-10-17T22:08:42.246042572Z [inf]  Starting scanner background thread...
2025-10-17T22:08:43.298073258Z [inf]  🎯 Hibrit Strateji başlatıldı: XRPUSDT (CRYPTO)
2025-10-17T22:08:43.298087104Z [inf]  🎯 Hibrit Strateji başlatıldı: 2ZUSDT (CRYPTO)
2025-10-17T22:08:43.298096153Z [inf]  🎯 Hibrit Strateji başlatıldı: TRXUSDT (CRYPTO)
2025-10-17T22:08:43.298103910Z [inf]  🎯 Hibrit Strateji başlatıldı: ADAUSDT (CRYPTO)
2025-10-17T22:08:43.298111807Z [inf]  🎯 Hibrit Strateji başlatıldı: PEPEUSDT (CRYPTO)
2025-10-17T22:08:43.298305683Z [inf]  ✓ Supabase'den 23 sinyal, 10 açık işlem yüklendi
2025-10-17T22:08:43.298310576Z [inf]  ✅ CCXT Binance bağlantısı başarılı
2025-10-17T22:08:43.298315376Z [inf]  🚀 Crypto Sinyal Tarayıcı başlatıldı! (TVDatafeed + Hybrid Strategy)
2025-10-17T22:08:43.298321233Z [inf]  ⏰ Tarama aralığı: 600 saniye (10.0 dakika)
2025-10-17T22:08:43.298326512Z [inf]  
2025-10-17T22:08:43.298331753Z [inf]  ======================================================================
2025-10-17T22:08:43.298338844Z [inf]  ### CRYPTO SİNYAL TARAYICI - HYBRID STRATEGY ###
2025-10-17T22:08:43.298343643Z [inf]  ======================================================================
2025-10-17T22:08:43.298349862Z [inf]  📋 pairs.md'den 449 USDT çifti yüklendi
2025-10-17T22:08:43.298355316Z [inf]  ✓ 449 kripto sembolü yüklendi
2025-10-17T22:08:43.298360147Z [inf]  🎯 Hibrit Strateji başlatıldı: BTCUSDT (CRYPTO)
2025-10-17T22:08:43.298365941Z [inf]  🎯 Hibrit Strateji başlatıldı: ETHUSDT (CRYPTO)
2025-10-17T22:08:43.298371981Z [inf]  🎯 Hibrit Strateji başlatıldı: SOLUSDT (CRYPTO)
2025-10-17T22:08:43.298376941Z [inf]  🎯 Hibrit Strateji başlatıldı: BNBUSDT (CRYPTO)
2025-10-17T22:08:43.298384324Z [inf]  🎯 Hibrit Strateji başlatıldı: USDCUSDT (CRYPTO)
2025-10-17T22:08:43.298390119Z [inf]  🎯 Hibrit Strateji başlatıldı: DOGEUSDT (CRYPTO)
2025-10-17T22:08:43.302093911Z [inf]  🎯 Hibrit Strateji başlatıldı: SUIUSDT (CRYPTO)
2025-10-17T22:08:43.302104577Z [inf]  🎯 Hibrit Strateji başlatıldı: ASTERUSDT (CRYPTO)
2025-10-17T22:08:43.302110859Z [inf]  🎯 Hibrit Strateji başlatıldı: OKBUSDT (CRYPTO)
2025-10-17T22:08:43.302117090Z [inf]  🎯 Hibrit Strateji başlatıldı: ENAUSDT (CRYPTO)
2025-10-17T22:08:43.302123380Z [inf]  🎯 Hibrit Strateji başlatıldı: XPLUSDT (CRYPTO)
2025-10-17T22:08:43.302130053Z [inf]  🎯 Hibrit Strateji başlatıldı: AVAXUSDT (CRYPTO)
2025-10-17T22:08:43.302142608Z [inf]  🎯 Hibrit Strateji başlatıldı: LINKUSDT (CRYPTO)
2025-10-17T22:08:43.302153239Z [inf]  🎯 Hibrit Strateji başlatıldı: LTCUSDT (CRYPTO)
2025-10-17T22:08:43.302162399Z [inf]  🎯 Hibrit Strateji başlatıldı: AAVEUSDT (CRYPTO)
2025-10-17T22:08:43.302169116Z [inf]  🎯 Hibrit Strateji başlatıldı: FDUSDUSDT (CRYPTO)
2025-10-17T22:08:43.302175354Z [inf]  🎯 Hibrit Strateji başlatıldı: MNTUSDT (CRYPTO)
2025-10-17T22:08:43.302182653Z [inf]  🎯 Hibrit Strateji başlatıldı: XAUTUSDT (CRYPTO)
2025-10-17T22:08:43.302190455Z [inf]  🎯 Hibrit Strateji başlatıldı: ZECUSDT (CRYPTO)
2025-10-17T22:08:43.302198423Z [inf]  🎯 Hibrit Strateji başlatıldı: HYPEUSDT (CRYPTO)
2025-10-17T22:08:43.302205237Z [inf]  🎯 Hibrit Strateji başlatıldı: USDEUSDT (CRYPTO)
2025-10-17T22:08:43.302211151Z [inf]  🎯 Hibrit Strateji başlatıldı: WIFUSDT (CRYPTO)
2025-10-17T22:08:43.302217501Z [inf]  🎯 Hibrit Strateji başlatıldı: PAXGUSDT (CRYPTO)
2025-10-17T22:08:43.302224915Z [inf]  🎯 Hibrit Strateji başlatıldı: YBUSDT (CRYPTO)
2025-10-17T22:08:43.302230996Z [inf]  🎯 Hibrit Strateji başlatıldı: APTUSDT (CRYPTO)
2025-10-17T22:08:43.302239321Z [inf]  🎯 Hibrit Strateji başlatıldı: TRUMPUSDT (CRYPTO)
2025-10-17T22:08:43.302248223Z [inf]  🎯 Hibrit Strateji başlatıldı: TAOUSDT (CRYPTO)
2025-10-17T22:08:43.303944337Z [inf]  🎯 Hibrit Strateji başlatıldı: ARBUSDT (CRYPTO)
2025-10-17T22:08:43.303952590Z [inf]  🎯 Hibrit Strateji başlatıldı: DOTUSDT (CRYPTO)
2025-10-17T22:08:43.303958914Z [inf]  🎯 Hibrit Strateji başlatıldı: UNIUSDT (CRYPTO)
2025-10-17T22:08:43.303965644Z [inf]  🎯 Hibrit Strateji başlatıldı: NEARUSDT (CRYPTO)
2025-10-17T22:08:43.303973860Z [inf]  🎯 Hibrit Strateji başlatıldı: CAKEUSDT (CRYPTO)
2025-10-17T22:08:43.303980678Z [inf]  🎯 Hibrit Strateji başlatıldı: KGENUSDT (CRYPTO)
2025-10-17T22:08:43.303986656Z [inf]  🎯 Hibrit Strateji başlatıldı: BLESSUSDT (CRYPTO)
2025-10-17T22:08:43.303993128Z [inf]  🎯 Hibrit Strateji başlatıldı: BCHUSDT (CRYPTO)
2025-10-17T22:08:43.304000303Z [inf]  🎯 Hibrit Strateji başlatıldı: XLMUSDT (CRYPTO)
2025-10-17T22:08:43.304006397Z [inf]  🎯 Hibrit Strateji başlatıldı: PENGUUSDT (CRYPTO)
2025-10-17T22:08:43.304013331Z [inf]  🎯 Hibrit Strateji başlatıldı: BONKUSDT (CRYPTO)
2025-10-17T22:08:43.304020320Z [inf]  🎯 Hibrit Strateji başlatıldı: BGBUSDT (CRYPTO)
2025-10-17T22:08:43.304028027Z [inf]  🎯 Hibrit Strateji başlatıldı: BELUSDT (CRYPTO)
2025-10-17T22:08:43.304034562Z [inf]  🎯 Hibrit Strateji başlatıldı: HBARUSDT (CRYPTO)
2025-10-17T22:08:43.304041466Z [inf]  🎯 Hibrit Strateji başlatıldı: CRVUSDT (CRYPTO)
2025-10-17T22:08:43.304048890Z [inf]  🎯 Hibrit Strateji başlatıldı: UGOLDUSDT (CRYPTO)
2025-10-17T22:08:43.304058805Z [inf]  🎯 Hibrit Strateji başlatıldı: COAIUSDT (CRYPTO)
2025-10-17T22:08:43.304065581Z [inf]  🎯 Hibrit Strateji başlatıldı: PUMPUSDT (CRYPTO)
2025-10-17T22:08:43.305227806Z [inf]  🎯 Hibrit Strateji başlatıldı: TONUSDT (CRYPTO)
2025-10-17T22:08:43.305235707Z [inf]  🎯 Hibrit Strateji başlatıldı: WLDUSDT (CRYPTO)
2025-10-17T22:08:43.305242072Z [inf]  🎯 Hibrit Strateji başlatıldı: LDOUSDT (CRYPTO)
2025-10-17T22:08:43.305247406Z [inf]  🎯 Hibrit Strateji başlatıldı: SNXUSDT (CRYPTO)
2025-10-17T22:08:43.305266908Z [inf]  🎯 Hibrit Strateji başlatıldı: XMRUSDT (CRYPTO)
2025-10-17T22:08:43.305273262Z [inf]  🎯 Hibrit Strateji başlatıldı: ONDOUSDT (CRYPTO)
2025-10-17T22:08:43.305285982Z [inf]  🎯 Hibrit Strateji başlatıldı: ETCUSDT (CRYPTO)
2025-10-17T22:08:43.305294892Z [inf]  🎯 Hibrit Strateji başlatıldı: SHIBUSDT (CRYPTO)
2025-10-17T22:08:43.305300945Z [inf]  🎯 Hibrit Strateji başlatıldı: SEIUSDT (CRYPTO)
2025-10-17T22:08:43.305306357Z [inf]  🎯 Hibrit Strateji başlatıldı: DASHUSDT (CRYPTO)
2025-10-17T22:08:43.305320537Z [inf]  🎯 Hibrit Strateji başlatıldı: FILUSDT (CRYPTO)
2025-10-17T22:08:43.305328472Z [inf]  🎯 Hibrit Strateji başlatıldı: OPUSDT (CRYPTO)
2025-10-17T22:08:43.305345835Z [inf]  🎯 Hibrit Strateji başlatıldı: YGGUSDT (CRYPTO)
2025-10-17T22:08:43.305352301Z [inf]  🎯 Hibrit Strateji başlatıldı: FETUSDT (CRYPTO)
2025-10-17T22:08:43.305359610Z [inf]  🎯 Hibrit Strateji başlatıldı: FORMUSDT (CRYPTO)
2025-10-17T22:08:43.305366465Z [inf]  🎯 Hibrit Strateji başlatıldı: PENDLEUSDT (CRYPTO)
2025-10-17T22:08:43.305373146Z [inf]  🎯 Hibrit Strateji başlatıldı: FARTCOINUSDT (CRYPTO)
2025-10-17T22:08:43.305375619Z [inf]  🎯 Hibrit Strateji başlatıldı: WLFIUSDT (CRYPTO)
2025-10-17T22:08:43.305407898Z [inf]  🎯 Hibrit Strateji başlatıldı: DEGOUSDT (CRYPTO)
2025-10-17T22:08:43.305416268Z [inf]  🎯 Hibrit Strateji başlatıldı: SUSDEUSDT (CRYPTO)
2025-10-17T22:08:43.309285804Z [inf]  🎯 Hibrit Strateji başlatıldı: EIGENUSDT (CRYPTO)
2025-10-17T22:08:43.309294303Z [inf]  🎯 Hibrit Strateji başlatıldı: ENSOUSDT (CRYPTO)
2025-10-17T22:08:43.309304898Z [inf]  🎯 Hibrit Strateji başlatıldı: FLOKIUSDT (CRYPTO)
2025-10-17T22:08:43.309311999Z [inf]  🎯 Hibrit Strateji başlatıldı: TAUSDT (CRYPTO)
2025-10-17T22:08:43.309320102Z [inf]  🎯 Hibrit Strateji başlatıldı: RECALLUSDT (CRYPTO)
2025-10-17T22:08:43.309327617Z [inf]  🎯 Hibrit Strateji başlatıldı: SOONUSDT (CRYPTO)
2025-10-17T22:08:43.309336117Z [inf]  🎯 Hibrit Strateji başlatıldı: LINEAUSDT (CRYPTO)
2025-10-17T22:08:43.309342863Z [inf]  🎯 Hibrit Strateji başlatıldı: IPUSDT (CRYPTO)
2025-10-17T22:08:43.309352052Z [inf]  🎯 Hibrit Strateji başlatıldı: HUSDT (CRYPTO)
2025-10-17T22:08:43.309359308Z [inf]  🎯 Hibrit Strateji başlatıldı: SUSDT (CRYPTO)
2025-10-17T22:08:43.309367011Z [inf]  🎯 Hibrit Strateji başlatıldı: POLUSDT (CRYPTO)
2025-10-17T22:08:43.309377268Z [inf]  🎯 Hibrit Strateji başlatıldı: ZORAUSDT (CRYPTO)
2025-10-17T22:08:43.309460096Z [inf]  🎯 Hibrit Strateji başlatıldı: FFUSDT (CRYPTO)
2025-10-17T22:08:43.309474882Z [inf]  🎯 Hibrit Strateji başlatıldı: VIRTUALUSDT (CRYPTO)
2025-10-17T22:08:43.309482818Z [inf]  🎯 Hibrit Strateji başlatıldı: SUPERUSDT (CRYPTO)
2025-10-17T22:08:43.309489294Z [inf]  🎯 Hibrit Strateji başlatıldı: GALAUSDT (CRYPTO)
2025-10-17T22:08:43.309496413Z [inf]  🎯 Hibrit Strateji başlatıldı: ATOMUSDT (CRYPTO)
2025-10-17T22:08:43.309506808Z [inf]  🎯 Hibrit Strateji başlatıldı: USD1USDT (CRYPTO)
2025-10-17T22:08:43.309515468Z [inf]  🎯 Hibrit Strateji başlatıldı: WUSDT (CRYPTO)
2025-10-17T22:08:43.315629330Z [inf]  🎯 Hibrit Strateji başlatıldı: TIAUSDT (CRYPTO)
2025-10-17T22:08:43.315637483Z [inf]  🎯 Hibrit Strateji başlatıldı: ALGOUSDT (CRYPTO)
2025-10-17T22:08:43.315643900Z [inf]  🎯 Hibrit Strateji başlatıldı: WALUSDT (CRYPTO)
2025-10-17T22:08:43.315651661Z [inf]  🎯 Hibrit Strateji başlatıldı: WBTUSDT (CRYPTO)
2025-10-17T22:08:43.315657361Z [inf]  🎯 Hibrit Strateji başlatıldı: WBTCUSDT (CRYPTO)
2025-10-17T22:08:43.315664384Z [inf]  🎯 Hibrit Strateji başlatıldı: INJUSDT (CRYPTO)
2025-10-17T22:08:43.315670900Z [inf]  🎯 Hibrit Strateji başlatıldı: OMUSDT (CRYPTO)
2025-10-17T22:08:43.315677405Z [inf]  🎯 Hibrit Strateji başlatıldı: KASUSDT (CRYPTO)
2025-10-17T22:08:43.315683358Z [inf]  🎯 Hibrit Strateji başlatıldı: ICPUSDT (CRYPTO)
2025-10-17T22:08:43.315688884Z [inf]  🎯 Hibrit Strateji başlatıldı: ETHFIUSDT (CRYPTO)
2025-10-17T22:08:43.315693789Z [inf]  🎯 Hibrit Strateji başlatıldı: USELESSUSDT (CRYPTO)
2025-10-17T22:08:43.315702059Z [inf]  🎯 Hibrit Strateji başlatıldı: RENDERUSDT (CRYPTO)
2025-10-17T22:08:43.315707730Z [inf]  🎯 Hibrit Strateji başlatıldı: DAIUSDT (CRYPTO)
2025-10-17T22:08:43.315713078Z [inf]  🎯 Hibrit Strateji başlatıldı: ATHUSDT (CRYPTO)
2025-10-17T22:08:43.315718752Z [inf]  🎯 Hibrit Strateji başlatıldı: PNUTUSDT (CRYPTO)
2025-10-17T22:08:43.315724672Z [inf]  🎯 Hibrit Strateji başlatıldı: MORPHOUSDT (CRYPTO)
2025-10-17T22:08:43.315729925Z [inf]  🎯 Hibrit Strateji başlatıldı: RSRUSDT (CRYPTO)
2025-10-17T22:08:43.315735875Z [inf]  🎯 Hibrit Strateji başlatıldı: BATUSDT (CRYPTO)
2025-10-17T22:08:43.315741268Z [inf]  🎯 Hibrit Strateji başlatıldı: ALICEUSDT (CRYPTO)
2025-10-17T22:08:43.321347949Z [inf]  🎯 Hibrit Strateji başlatıldı: PROVEUSDT (CRYPTO)
2025-10-17T22:08:43.321357531Z [inf]  🎯 Hibrit Strateji başlatıldı: LAUSDT (CRYPTO)
2025-10-17T22:08:43.321364810Z [inf]  🎯 Hibrit Strateji başlatıldı: TWTUSDT (CRYPTO)
2025-10-17T22:08:43.321372440Z [inf]  🎯 Hibrit Strateji başlatıldı: STETHUSDT (CRYPTO)
2025-10-17T22:08:43.321398373Z [inf]  🎯 Hibrit Strateji başlatıldı: BUSDT (CRYPTO)
2025-10-17T22:08:43.321407729Z [inf]  🎯 Hibrit Strateji başlatıldı: IMXUSDT (CRYPTO)
2025-10-17T22:08:43.321414216Z [inf]  🎯 Hibrit Strateji başlatıldı: ENSUSDT (CRYPTO)
2025-10-17T22:08:43.321420332Z [inf]  🎯 Hibrit Strateji başlatıldı: WCTUSDT (CRYPTO)
2025-10-17T22:08:43.321426249Z [inf]  🎯 Hibrit Strateji başlatıldı: RDNTUSDT (CRYPTO)
2025-10-17T22:08:43.321433526Z [inf]  🎯 Hibrit Strateji başlatıldı: AUSDTUSDT (CRYPTO)
2025-10-17T22:08:43.321439740Z [inf]  🎯 Hibrit Strateji başlatıldı: ARPAUSDT (CRYPTO)
2025-10-17T22:08:43.321446407Z [inf]  🎯 Hibrit Strateji başlatıldı: ZENUSDT (CRYPTO)
2025-10-17T22:08:43.321452304Z [inf]  🎯 Hibrit Strateji başlatıldı: LABUSDT (CRYPTO)
2025-10-17T22:08:43.321458956Z [inf]  🎯 Hibrit Strateji başlatıldı: HEIUSDT (CRYPTO)
2025-10-17T22:08:43.321465402Z [inf]  🎯 Hibrit Strateji başlatıldı: SYRUPUSDT (CRYPTO)
2025-10-17T22:08:43.321472318Z [inf]  🎯 Hibrit Strateji başlatıldı: BERAUSDT (CRYPTO)
2025-10-17T22:08:43.321478282Z [inf]  🎯 Hibrit Strateji başlatıldı: HOOKUSDT (CRYPTO)
2025-10-17T22:08:43.321484030Z [inf]  🎯 Hibrit Strateji başlatıldı: ARKMUSDT (CRYPTO)
2025-10-17T22:08:43.321489304Z [inf]  🎯 Hibrit Strateji başlatıldı: OGUSDT (CRYPTO)
2025-10-17T22:08:43.321495094Z [inf]  🎯 Hibrit Strateji başlatıldı: LAUNCHCO...USDT (CRYPTO)
2025-10-17T22:08:43.325240858Z [inf]  🎯 Hibrit Strateji başlatıldı: BRETTUSDT (CRYPTO)
2025-10-17T22:08:43.325252034Z [inf]  🎯 Hibrit Strateji başlatıldı: RAYUSDT (CRYPTO)
2025-10-17T22:08:43.325262490Z [inf]  🎯 Hibrit Strateji başlatıldı: STRKUSDT (CRYPTO)
2025-10-17T22:08:43.325269627Z [inf]  🎯 Hibrit Strateji başlatıldı: MYXUSDT (CRYPTO)
2025-10-17T22:08:43.325276446Z [inf]  🎯 Hibrit Strateji başlatıldı: ORDIUSDT (CRYPTO)
2025-10-17T22:08:43.325285764Z [inf]  🎯 Hibrit Strateji başlatıldı: AXSUSDT (CRYPTO)
2025-10-17T22:08:43.325293249Z [inf]  🎯 Hibrit Strateji başlatıldı: BBUSDT (CRYPTO)
2025-10-17T22:08:43.325300054Z [inf]  🎯 Hibrit Strateji başlatıldı: B2USDT (CRYPTO)
2025-10-17T22:08:43.325306021Z [inf]  🎯 Hibrit Strateji başlatıldı: EDUUSDT (CRYPTO)
2025-10-17T22:08:43.325311754Z [inf]  🎯 Hibrit Strateji başlatıldı: XDCUSDT (CRYPTO)
2025-10-17T22:08:43.325316735Z [inf]  🎯 Hibrit Strateji başlatıldı: OPENUSDT (CRYPTO)
2025-10-17T22:08:43.325322668Z [inf]  🎯 Hibrit Strateji başlatıldı: AVNTUSDT (CRYPTO)
2025-10-17T22:08:43.325329348Z [inf]  🎯 Hibrit Strateji başlatıldı: SANDUSDT (CRYPTO)
2025-10-17T22:08:43.325334087Z [inf]  🎯 Hibrit Strateji başlatıldı: SUNUSDT (CRYPTO)
2025-10-17T22:08:43.325339202Z [inf]  🎯 Hibrit Strateji başlatıldı: ZROUSDT (CRYPTO)
2025-10-17T22:08:43.325345700Z [inf]  🎯 Hibrit Strateji başlatıldı: APEUSDT (CRYPTO)
2025-10-17T22:08:43.325350019Z [inf]  🎯 Hibrit Strateji başlatıldı: VETUSDT (CRYPTO)
2025-10-17T22:08:43.325355379Z [inf]  🎯 Hibrit Strateji başlatıldı: PEOPLEUSDT (CRYPTO)
2025-10-17T22:08:43.325359835Z [inf]  🎯 Hibrit Strateji başlatıldı: JSTUSDT (CRYPTO)
2025-10-17T22:08:43.329048829Z [inf]  🎯 Hibrit Strateji başlatıldı: 0GUSDT (CRYPTO)
2025-10-17T22:08:43.329065297Z [inf]  🎯 Hibrit Strateji başlatıldı: AUSDT (CRYPTO)
2025-10-17T22:08:43.329075717Z [inf]  🎯 Hibrit Strateji başlatıldı: BIOUSDT (CRYPTO)
2025-10-17T22:08:43.329084596Z [inf]  🎯 Hibrit Strateji başlatıldı: GRASSUSDT (CRYPTO)
2025-10-17T22:08:43.329093267Z [inf]  🎯 Hibrit Strateji başlatıldı: AIUSDT (CRYPTO)
2025-10-17T22:08:43.329102254Z [inf]  🎯 Hibrit Strateji başlatıldı: PYTHUSDT (CRYPTO)
2025-10-17T22:08:43.329113393Z [inf]  🎯 Hibrit Strateji başlatıldı: SPKUSDT (CRYPTO)
2025-10-17T22:08:43.329121072Z [inf]  🎯 Hibrit Strateji başlatıldı: NEIROUSDT (CRYPTO)
2025-10-17T22:08:43.329130689Z [inf]  🎯 Hibrit Strateji başlatıldı: AI16ZUSDT (CRYPTO)
2025-10-17T22:08:43.329141301Z [inf]  🎯 Hibrit Strateji başlatıldı: COMPUSDT (CRYPTO)
2025-10-17T22:08:43.329150370Z [inf]  🎯 Hibrit Strateji başlatıldı: JTOUSDT (CRYPTO)
2025-10-17T22:08:43.329159813Z [inf]  🎯 Hibrit Strateji başlatıldı: USDRUSDT (CRYPTO)
2025-10-17T22:08:43.329171929Z [inf]  🎯 Hibrit Strateji başlatıldı: BARDUSDT (CRYPTO)
2025-10-17T22:08:43.329180235Z [inf]  🎯 Hibrit Strateji başlatıldı: SUSHIUSDT (CRYPTO)
2025-10-17T22:08:43.329188130Z [inf]  🎯 Hibrit Strateji başlatıldı: CATIUSDT (CRYPTO)
2025-10-17T22:08:43.329195481Z [inf]  🎯 Hibrit Strateji başlatıldı: HOLOUSDT (CRYPTO)
2025-10-17T22:08:43.329649572Z [inf]  🎯 Hibrit Strateji başlatıldı: SOLVUSDT (CRYPTO)
2025-10-17T22:08:43.329658915Z [inf]  🎯 Hibrit Strateji başlatıldı: MANAUSDT (CRYPTO)
2025-10-17T22:08:43.329670030Z [inf]  🎯 Hibrit Strateji başlatıldı: ZKCUSDT (CRYPTO)
2025-10-17T22:08:43.329678855Z [inf]  🎯 Hibrit Strateji başlatıldı: XUSDUSDT (CRYPTO)
2025-10-17T22:08:43.329687125Z [inf]  🎯 Hibrit Strateji başlatıldı: CLOUSDT (CRYPTO)
2025-10-17T22:08:43.333268378Z [inf]  🎯 Hibrit Strateji başlatıldı: XPINUSDT (CRYPTO)
2025-10-17T22:08:43.333277638Z [inf]  🎯 Hibrit Strateji başlatıldı: JUPUSDT (CRYPTO)
2025-10-17T22:08:43.333286630Z [inf]  🎯 Hibrit Strateji başlatıldı: POPCATUSDT (CRYPTO)
2025-10-17T22:08:43.333300962Z [inf]  🎯 Hibrit Strateji başlatıldı: PLUMEUSDT (CRYPTO)
2025-10-17T22:08:43.333314287Z [inf]  🎯 Hibrit Strateji başlatıldı: ARUSDT (CRYPTO)
2025-10-17T22:08:43.333323042Z [inf]  🎯 Hibrit Strateji başlatıldı: TUTUSDT (CRYPTO)
2025-10-17T22:08:43.333332170Z [inf]  🎯 Hibrit Strateji başlatıldı: ABUSDT (CRYPTO)
2025-10-17T22:08:43.333341179Z [inf]  🎯 Hibrit Strateji başlatıldı: BOMEUSDT (CRYPTO)
2025-10-17T22:08:43.333350521Z [inf]  🎯 Hibrit Strateji başlatıldı: KAIAUSDT (CRYPTO)
2025-10-17T22:08:43.333364930Z [inf]  🎯 Hibrit Strateji başlatıldı: RUNEUSDT (CRYPTO)
2025-10-17T22:08:43.333371674Z [inf]  🎯 Hibrit Strateji başlatıldı: KERNELUSDT (CRYPTO)
2025-10-17T22:08:43.333399410Z [inf]  🎯 Hibrit Strateji başlatıldı: PIUSDT (CRYPTO)
2025-10-17T22:08:43.333413328Z [inf]  🎯 Hibrit Strateji başlatıldı: TURBOUSDT (CRYPTO)
2025-10-17T22:08:43.333421638Z [inf]  🎯 Hibrit Strateji başlatıldı: LUNAUSDT (CRYPTO)
2025-10-17T22:08:43.333429483Z [inf]  🎯 Hibrit Strateji başlatıldı: CYBERUSDT (CRYPTO)
2025-10-17T22:08:43.333437023Z [inf]  🎯 Hibrit Strateji başlatıldı: STOUSDT (CRYPTO)
2025-10-17T22:08:43.333446747Z [inf]  🎯 Hibrit Strateji başlatıldı: 1INCHUSDT (CRYPTO)
2025-10-17T22:08:43.333454663Z [inf]  🎯 Hibrit Strateji başlatıldı: CHZUSDT (CRYPTO)
2025-10-17T22:08:43.333467076Z [inf]  🎯 Hibrit Strateji başlatıldı: 4USDT (CRYPTO)
2025-10-17T22:08:43.333475709Z [inf]  🎯 Hibrit Strateji başlatıldı: IOUSDT (CRYPTO)
2025-10-17T22:08:43.333484601Z [inf]  🎯 Hibrit Strateji başlatıldı: GRTUSDT (CRYPTO)
2025-10-17T22:08:43.337525224Z [inf]  🎯 Hibrit Strateji başlatıldı: ALCHUSDT (CRYPTO)
2025-10-17T22:08:43.337532730Z [inf]  🎯 Hibrit Strateji başlatıldı: GMTUSDT (CRYPTO)
2025-10-17T22:08:43.337540434Z [inf]  🎯 Hibrit Strateji başlatıldı: NMRUSDT (CRYPTO)
2025-10-17T22:08:43.337546057Z [inf]  🎯 Hibrit Strateji başlatıldı: XANUSDT (CRYPTO)
2025-10-17T22:08:43.337557356Z [inf]  🎯 Hibrit Strateji başlatıldı: MIRAUSDT (CRYPTO)
2025-10-17T22:08:43.337564057Z [inf]  🎯 Hibrit Strateji başlatıldı: CFXUSDT (CRYPTO)
2025-10-17T22:08:43.337570947Z [inf]  🎯 Hibrit Strateji başlatıldı: MBGUSDT (CRYPTO)
2025-10-17T22:08:43.337578624Z [inf]  🎯 Hibrit Strateji başlatıldı: MOODENGUSDT (CRYPTO)
2025-10-17T22:08:43.337586243Z [inf]  🎯 Hibrit Strateji başlatıldı: JASMYUSDT (CRYPTO)
2025-10-17T22:08:43.337593124Z [inf]  🎯 Hibrit Strateji başlatıldı: HOMEUSDT (CRYPTO)
2025-10-17T22:08:43.337600193Z [inf]  🎯 Hibrit Strateji başlatıldı: REDUSDT (CRYPTO)
2025-10-17T22:08:43.337608849Z [inf]  🎯 Hibrit Strateji başlatıldı: ARIAUSDT (CRYPTO)
2025-10-17T22:08:43.337622336Z [inf]  🎯 Hibrit Strateji başlatıldı: MAGICUSDT (CRYPTO)
2025-10-17T22:08:43.337631299Z [inf]  🎯 Hibrit Strateji başlatıldı: MEWUSDT (CRYPTO)
2025-10-17T22:08:43.337637522Z [inf]  🎯 Hibrit Strateji başlatıldı: VRAUSDT (CRYPTO)
2025-10-17T22:08:43.337643364Z [inf]  🎯 Hibrit Strateji başlatıldı: MEMEUSDT (CRYPTO)
2025-10-17T22:08:43.337649992Z [inf]  🎯 Hibrit Strateji başlatıldı: MASKUSDT (CRYPTO)
2025-10-17T22:08:43.337655829Z [inf]  🎯 Hibrit Strateji başlatıldı: DRIFTUSDT (CRYPTO)
2025-10-17T22:08:43.337666849Z [inf]  🎯 Hibrit Strateji başlatıldı: ETHDYDXUSDT (CRYPTO)
2025-10-17T22:08:43.337673782Z [inf]  🎯 Hibrit Strateji başlatıldı: YFIUSDT (CRYPTO)
2025-10-17T22:08:43.340901111Z [inf]  🎯 Hibrit Strateji başlatıldı: INITUSDT (CRYPTO)
2025-10-17T22:08:43.340901387Z [inf]  🎯 Hibrit Strateji başlatıldı: BASUSDT (CRYPTO)
2025-10-17T22:08:43.340912754Z [inf]  🎯 Hibrit Strateji başlatıldı: ANIMEUSDT (CRYPTO)
2025-10-17T22:08:43.340925115Z [inf]  🎯 Hibrit Strateji başlatıldı: ACTUSDT (CRYPTO)
2025-10-17T22:08:43.340927068Z [inf]  🎯 Hibrit Strateji başlatıldı: TRBUSDT (CRYPTO)
2025-10-17T22:08:43.340938534Z [inf]  🎯 Hibrit Strateji başlatıldı: ZBCNUSDT (CRYPTO)
2025-10-17T22:08:43.340943843Z [inf]  🎯 Hibrit Strateji başlatıldı: TOSHIUSDT (CRYPTO)
2025-10-17T22:08:43.340951296Z [inf]  🎯 Hibrit Strateji başlatıldı: SHELLUSDT (CRYPTO)
2025-10-17T22:08:43.340960937Z [inf]  🎯 Hibrit Strateji başlatıldı: STBLUSDT (CRYPTO)
2025-10-17T22:08:43.340969228Z [inf]  🎯 Hibrit Strateji başlatıldı: ZKUSDT (CRYPTO)
2025-10-17T22:08:43.340975028Z [inf]  🎯 Hibrit Strateji başlatıldı: SOMIUSDT (CRYPTO)
2025-10-17T22:08:43.340984625Z [inf]  🎯 Hibrit Strateji başlatıldı: AEVOUSDT (CRYPTO)
2025-10-17T22:08:43.340995273Z [inf]  🎯 Hibrit Strateji başlatıldı: ZEREBROUSDT (CRYPTO)
2025-10-17T22:08:43.340996846Z [inf]  🎯 Hibrit Strateji başlatıldı: APEXUSDT (CRYPTO)
2025-10-17T22:08:43.341007542Z [inf]  🎯 Hibrit Strateji başlatıldı: MOVEUSDT (CRYPTO)
2025-10-17T22:08:43.341014208Z [inf]  🎯 Hibrit Strateji başlatıldı: STEEMUSDT (CRYPTO)
2025-10-17T22:08:43.341021062Z [inf]  🎯 Hibrit Strateji başlatıldı: REALUSDT (CRYPTO)
2025-10-17T22:08:43.341027076Z [inf]  🎯 Hibrit Strateji başlatıldı: THETAUSDT (CRYPTO)
2025-10-17T22:08:43.341034113Z [inf]  🎯 Hibrit Strateji başlatıldı: PTBUSDT (CRYPTO)
2025-10-17T22:08:43.341041455Z [inf]  🎯 Hibrit Strateji başlatıldı: MERLUSDT (CRYPTO)
2025-10-17T22:08:43.341048420Z [inf]  🎯 Hibrit Strateji başlatıldı: KUSDT (CRYPTO)
2025-10-17T22:08:43.344064142Z [inf]  🎯 Hibrit Strateji başlatıldı: PRCLUSDT (CRYPTO)
2025-10-17T22:08:43.344078387Z [inf]  🎯 Hibrit Strateji başlatıldı: DEXEUSDT (CRYPTO)
2025-10-17T22:08:43.344086793Z [inf]  🎯 Hibrit Strateji başlatıldı: FUSDT (CRYPTO)
2025-10-17T22:08:43.344092943Z [inf]  🎯 Hibrit Strateji başlatıldı: RATSUSDT (CRYPTO)
2025-10-17T22:08:43.344099398Z [inf]  🎯 Hibrit Strateji başlatıldı: HUMAUSDT (CRYPTO)
2025-10-17T22:08:43.344105684Z [inf]  🎯 Hibrit Strateji başlatıldı: CROUSDT (CRYPTO)
2025-10-17T22:08:43.344111814Z [inf]  🎯 Hibrit Strateji başlatıldı: AMPUSDT (CRYPTO)
2025-10-17T22:08:43.344118226Z [inf]  🎯 Hibrit Strateji başlatıldı: HAEDALUSDT (CRYPTO)
2025-10-17T22:08:43.344123836Z [inf]  🎯 Hibrit Strateji başlatıldı: VANAUSDT (CRYPTO)
2025-10-17T22:08:43.344129753Z [inf]  🎯 Hibrit Strateji başlatıldı: APEPEUSDT (CRYPTO)
2025-10-17T22:08:43.344135200Z [inf]  🎯 Hibrit Strateji başlatıldı: CHRUSDT (CRYPTO)
2025-10-17T22:08:43.344142075Z [inf]  🎯 Hibrit Strateji başlatıldı: TREEUSDT (CRYPTO)
2025-10-17T22:08:43.344152421Z [inf]  🎯 Hibrit Strateji başlatıldı: EDENUSDT (CRYPTO)
2025-10-17T22:08:43.344158713Z [inf]  🎯 Hibrit Strateji başlatıldı: SAHARAUSDT (CRYPTO)
2025-10-17T22:08:43.344165882Z [inf]  🎯 Hibrit Strateji başlatıldı: KAITOUSDT (CRYPTO)
2025-10-17T22:08:43.344172677Z [inf]  🎯 Hibrit Strateji başlatıldı: SPXUSDT (CRYPTO)
2025-10-17T22:08:43.344179866Z [inf]  🎯 Hibrit Strateji başlatıldı: WETHUSDT (CRYPTO)
2025-10-17T22:08:43.344187636Z [inf]  🎯 Hibrit Strateji başlatıldı: QNTUSDT (CRYPTO)
2025-10-17T22:08:43.344194286Z [inf]  🎯 Hibrit Strateji başlatıldı: EULUSDT (CRYPTO)
2025-10-17T22:08:43.344200988Z [inf]  🎯 Hibrit Strateji başlatıldı: PARTIUSDT (CRYPTO)
2025-10-17T22:08:43.344207118Z [inf]  🎯 Hibrit Strateji başlatıldı: SSVUSDT (CRYPTO)
2025-10-17T22:08:43.348239059Z [inf]  🎯 Hibrit Strateji başlatıldı: USTCUSDT (CRYPTO)
2025-10-17T22:08:43.348248568Z [inf]  🎯 Hibrit Strateji başlatıldı: AEROUSDT (CRYPTO)
2025-10-17T22:08:43.348258262Z [inf]  🎯 Hibrit Strateji başlatıldı: ALTUSDT (CRYPTO)
2025-10-17T22:08:43.348265409Z [inf]  🎯 Hibrit Strateji başlatıldı: AIXBTUSDT (CRYPTO)
2025-10-17T22:08:43.348270837Z [inf]  🎯 Hibrit Strateji başlatıldı: NOTUSDT (CRYPTO)
2025-10-17T22:08:43.348275993Z [inf]  🎯 Hibrit Strateji başlatıldı: RAREUSDT (CRYPTO)
2025-10-17T22:08:43.348283327Z [inf]  🎯 Hibrit Strateji başlatıldı: XTUSDT (CRYPTO)
2025-10-17T22:08:43.348287322Z [inf]  🎯 Hibrit Strateji başlatıldı: STXUSDT (CRYPTO)
2025-10-17T22:08:43.348292597Z [inf]  🎯 Hibrit Strateji başlatıldı: API3USDT (CRYPTO)
2025-10-17T22:08:43.348296740Z [inf]  🎯 Hibrit Strateji başlatıldı: DOODUSDT (CRYPTO)
2025-10-17T22:08:43.348301423Z [inf]  🎯 Hibrit Strateji başlatıldı: NEOUSDT (CRYPTO)
2025-10-17T22:08:43.348305599Z [inf]  🎯 Hibrit Strateji başlatıldı: USDQUSDT (CRYPTO)
2025-10-17T22:08:43.348310980Z [inf]  🎯 Hibrit Strateji başlatıldı: MBOXUSDT (CRYPTO)
2025-10-17T22:08:43.348315514Z [inf]  🎯 Hibrit Strateji başlatıldı: SONICUSDT (CRYPTO)
2025-10-17T22:08:43.348320041Z [inf]  🎯 Hibrit Strateji başlatıldı: LISTAUSDT (CRYPTO)
2025-10-17T22:08:43.348324861Z [inf]  🎯 Hibrit Strateji başlatıldı: XTZUSDT (CRYPTO)
2025-10-17T22:08:43.348328894Z [inf]  🎯 Hibrit Strateji başlatıldı: ILVUSDT (CRYPTO)
2025-10-17T22:08:43.348333496Z [inf]  🎯 Hibrit Strateji başlatıldı: LUNCUSDT (CRYPTO)
2025-10-17T22:08:43.348339649Z [inf]  🎯 Hibrit Strateji başlatıldı: FLKUSDT (CRYPTO)
2025-10-17T22:08:43.348344551Z [inf]  🎯 Hibrit Strateji başlatıldı: CLANKERUSDT (CRYPTO)
2025-10-17T22:08:43.348350461Z [inf]  🎯 Hibrit Strateji başlatıldı: SQDUSDT (CRYPTO)
2025-10-17T22:08:43.356565167Z [inf]  🎯 Hibrit Strateji başlatıldı: VELOUSDT (CRYPTO)
2025-10-17T22:08:43.356578631Z [inf]  🎯 Hibrit Strateji başlatıldı: NILUSDT (CRYPTO)
2025-10-17T22:08:43.356583503Z [inf]  🎯 Hibrit Strateji başlatıldı: CELOUSDT (CRYPTO)
2025-10-17T22:08:43.356593789Z [inf]  🎯 Hibrit Strateji başlatıldı: NEXOUSDT (CRYPTO)
2025-10-17T22:08:43.356608266Z [inf]  🎯 Hibrit Strateji başlatıldı: BFUSDUSDT (CRYPTO)
2025-10-17T22:08:43.356608478Z [inf]  🎯 Hibrit Strateji başlatıldı: AITECHUSDT (CRYPTO)
2025-10-17T22:08:43.356618915Z [inf]  🎯 Hibrit Strateji başlatıldı: BTTUSDT (CRYPTO)
2025-10-17T22:08:43.356628570Z [inf]  🎯 Hibrit Strateji başlatıldı: UMAUSDT (CRYPTO)
2025-10-17T22:08:43.356642441Z [inf]  🎯 Hibrit Strateji başlatıldı: DYDXUSDT (CRYPTO)
2025-10-17T22:08:43.356644345Z [inf]  🎯 Hibrit Strateji başlatıldı: $MBGUSDT (CRYPTO)
2025-10-17T22:08:43.356659781Z [inf]  🎯 Hibrit Strateji başlatıldı: CVXUSDT (CRYPTO)
2025-10-17T22:08:43.356660459Z [inf]  🎯 Hibrit Strateji başlatıldı: ACHUSDT (CRYPTO)
2025-10-17T22:08:43.356675111Z [inf]  🎯 Hibrit Strateji başlatıldı: HYPERUSDT (CRYPTO)
2025-10-17T22:08:43.356678774Z [inf]  🎯 Hibrit Strateji başlatıldı: MINAUSDT (CRYPTO)
2025-10-17T22:08:43.356688954Z [inf]  🎯 Hibrit Strateji başlatıldı: VINEUSDT (CRYPTO)
2025-10-17T22:08:43.356693889Z [inf]  🎯 Hibrit Strateji başlatıldı: ERAUSDT (CRYPTO)
2025-10-17T22:08:43.356701345Z [inf]  🎯 Hibrit Strateji başlatıldı: FTNUSDT (CRYPTO)
2025-10-17T22:08:43.356708964Z [inf]  🎯 Hibrit Strateji başlatıldı: REZUSDT (CRYPTO)
2025-10-17T22:08:43.356715776Z [inf]  🎯 Hibrit Strateji başlatıldı: HANAUSDT (CRYPTO)
2025-10-17T22:08:43.356722990Z [inf]  🎯 Hibrit Strateji başlatıldı: NXPCUSDT (CRYPTO)
2025-10-17T22:08:43.356731106Z [inf]  🎯 Hibrit Strateji başlatıldı: CETUSUSDT (CRYPTO)
2025-10-17T22:08:43.359941675Z [inf]  🎯 Hibrit Strateji başlatıldı: BSVUSDT (CRYPTO)
2025-10-17T22:08:43.359952181Z [inf]  🎯 Hibrit Strateji başlatıldı: A2ZUSDT (CRYPTO)
2025-10-17T22:08:43.359960101Z [inf]  🎯 Hibrit Strateji başlatıldı: EGLDUSDT (CRYPTO)
2025-10-17T22:08:43.359969908Z [inf]  🎯 Hibrit Strateji başlatıldı: FTTUSDT (CRYPTO)
2025-10-17T22:08:43.359978943Z [inf]  🎯 Hibrit Strateji başlatıldı: CARVUSDT (CRYPTO)
2025-10-17T22:08:43.359986893Z [inf]  🎯 Hibrit Strateji başlatıldı: LPTUSDT (CRYPTO)
2025-10-17T22:08:43.359994342Z [inf]  🎯 Hibrit Strateji başlatıldı: BEAMUSDT (CRYPTO)
2025-10-17T22:08:43.360002830Z [inf]  🎯 Hibrit Strateji başlatıldı: AVLUSDT (CRYPTO)
2025-10-17T22:08:43.360012072Z [inf]  🎯 Hibrit Strateji başlatıldı: ORDERUSDT (CRYPTO)
2025-10-17T22:08:43.360018709Z [inf]  🎯 Hibrit Strateji başlatıldı: IOTXUSDT (CRYPTO)
2025-10-17T22:08:43.360026820Z [inf]  🎯 Hibrit Strateji başlatıldı: IDUSDT (CRYPTO)
2025-10-17T22:08:43.360034610Z [inf]  🎯 Hibrit Strateji başlatıldı: ANKRUSDT (CRYPTO)
2025-10-17T22:08:43.360044781Z [inf]  🎯 Hibrit Strateji başlatıldı: XAIUSDT (CRYPTO)
2025-10-17T22:08:43.360052419Z [inf]  🎯 Hibrit Strateji başlatıldı: MUBARAKUSDT (CRYPTO)
2025-10-17T22:08:43.360061052Z [inf]  🎯 Hibrit Strateji başlatıldı: PUFFERUSDT (CRYPTO)
2025-10-17T22:08:43.360069699Z [inf]  🎯 Hibrit Strateji başlatıldı: HFTUSDT (CRYPTO)
2025-10-17T22:08:43.360078771Z [inf]  🎯 Hibrit Strateji başlatıldı: BABYUSDT (CRYPTO)
2025-10-17T22:08:43.360086118Z [inf]  🎯 Hibrit Strateji başlatıldı: ESUSDT (CRYPTO)
2025-10-17T22:08:43.360093503Z [inf]  🎯 Hibrit Strateji başlatıldı: MPRAUSDT (CRYPTO)
2025-10-17T22:08:43.360101352Z [inf]  🎯 Hibrit Strateji başlatıldı: TOWNSUSDT (CRYPTO)
2025-10-17T22:08:43.362907056Z [inf]  🎯 Hibrit Strateji başlatıldı: JELLYJEL...USDT (CRYPTO)
2025-10-17T22:08:43.362919463Z [inf]  🎯 Hibrit Strateji başlatıldı: HTXUSDT (CRYPTO)
2025-10-17T22:08:43.362928740Z [inf]  🎯 Hibrit Strateji başlatıldı: SUNDOGUSDT (CRYPTO)
2025-10-17T22:08:43.362937901Z [inf]  🎯 Hibrit Strateji başlatıldı: CTCUSDT (CRYPTO)
2025-10-17T22:08:43.362951022Z [inf]  🎯 Hibrit Strateji başlatıldı: ASTRUSDT (CRYPTO)
2025-10-17T22:08:43.362966021Z [inf]  🎯 Hibrit Strateji başlatıldı: DEGENUSDT (CRYPTO)
2025-10-17T22:08:43.362973739Z [inf]  🎯 Hibrit Strateji başlatıldı: ZRXUSDT (CRYPTO)
2025-10-17T22:08:43.362981190Z [inf]  🎯 Hibrit Strateji başlatıldı: SKYUSDT (CRYPTO)
2025-10-17T22:08:43.362988411Z [inf]  🎯 Hibrit Strateji başlatıldı: B3USDT (CRYPTO)
2025-10-17T22:08:43.362996432Z [inf]  🎯 Hibrit Strateji başlatıldı: BLURUSDT (CRYPTO)
2025-10-17T22:08:43.363003578Z [inf]  🎯 Hibrit Strateji başlatıldı: PROMPTUSDT (CRYPTO)
2025-10-17T22:08:43.363012034Z [inf]  🎯 Hibrit Strateji başlatıldı: MOCAUSDT (CRYPTO)
2025-10-17T22:08:43.363018852Z [inf]  🎯 Hibrit Strateji başlatıldı: AXLUSDT (CRYPTO)
2025-10-17T22:08:43.363027083Z [inf]  🎯 Hibrit Strateji başlatıldı: IKAUSDT (CRYPTO)
2025-10-17T22:08:43.363034248Z [inf]  🎯 Hibrit Strateji başlatıldı: LAYERUSDT (CRYPTO)
2025-10-17T22:08:43.363041796Z [inf]  🎯 Hibrit Strateji başlatıldı: XYOUSDT (CRYPTO)
2025-10-17T22:08:43.363048456Z [inf]  🎯 Hibrit Strateji başlatıldı: IDOLUSDT (CRYPTO)
2025-10-17T22:08:43.363055823Z [inf]  🎯 Hibrit Strateji başlatıldı: KAVAUSDT (CRYPTO)
2025-10-17T22:08:43.363062697Z [inf]  🎯 Hibrit Strateji başlatıldı: FRAXUSDT (CRYPTO)
2025-10-17T22:08:43.363072736Z [inf]  🎯 Hibrit Strateji başlatıldı: BROCCOLIUSDT (CRYPTO)
2025-10-17T22:08:43.363079661Z [inf]  🎯 Hibrit Strateji başlatıldı: IOTAUSDT (CRYPTO)
2025-10-17T22:08:43.366461868Z [inf]  🎯 Hibrit Strateji başlatıldı: XIONUSDT (CRYPTO)
2025-10-17T22:08:43.366463970Z [inf]  🎯 Hibrit Strateji başlatıldı: MOGUSDT (CRYPTO)
2025-10-17T22:08:43.366478519Z [inf]  🎯 Hibrit Strateji başlatıldı: TSLAXUSDT (CRYPTO)
2025-10-17T22:08:43.366484781Z [inf]  🎯 Hibrit Strateji başlatıldı: GOATUSDT (CRYPTO)
2025-10-17T22:08:43.366490416Z [inf]  🎯 Hibrit Strateji başlatıldı: COREUSDT (CRYPTO)
2025-10-17T22:08:43.366503055Z [inf]  🎯 Hibrit Strateji başlatıldı: WOOUSDT (CRYPTO)
2025-10-17T22:08:43.366503759Z [inf]  🎯 Hibrit Strateji başlatıldı: KMNOUSDT (CRYPTO)
2025-10-17T22:08:43.366517484Z [inf]  🎯 Hibrit Strateji başlatıldı: COOKIEUSDT (CRYPTO)
2025-10-17T22:08:43.366520822Z [inf]  🎯 Hibrit Strateji başlatıldı: BIGTIMEUSDT (CRYPTO)
2025-10-17T22:08:43.366530097Z [inf]  🎯 Hibrit Strateji başlatıldı: SKATEUSDT (CRYPTO)
2025-10-17T22:08:43.366536461Z [inf]  🎯 Hibrit Strateji başlatıldı: C98USDT (CRYPTO)
2025-10-17T22:08:43.366543385Z [inf]  🎯 Hibrit Strateji başlatıldı: RDACUSDT (CRYPTO)
2025-10-17T22:08:43.366554403Z [inf]  🎯 Hibrit Strateji başlatıldı: ICEUSDT (CRYPTO)
2025-10-17T22:08:43.366555495Z [inf]  🎯 Hibrit Strateji başlatıldı: NFTUSDT (CRYPTO)
2025-10-17T22:08:43.366566260Z [inf]  🎯 Hibrit Strateji başlatıldı: GAIAUSDT (CRYPTO)
2025-10-17T22:08:43.366574274Z [inf]  🎯 Hibrit Strateji başlatıldı: AGLDUSDT (CRYPTO)
2025-10-17T22:08:43.366578204Z [inf]  🎯 Hibrit Strateji başlatıldı: CGPTUSDT (CRYPTO)
2025-10-17T22:08:43.366583846Z [inf]  🎯 Hibrit Strateji başlatıldı: CRCLXUSDT (CRYPTO)
2025-10-17T22:08:43.366589625Z [inf]  🎯 Hibrit Strateji başlatıldı: IOSTUSDT (CRYPTO)
2025-10-17T22:08:43.366598275Z [inf]  🎯 Hibrit Strateji başlatıldı: SUSDSUSDT (CRYPTO)
2025-10-17T22:08:43.366606708Z [inf]  🎯 Hibrit Strateji başlatıldı: USUALUSDT (CRYPTO)
2025-10-17T22:08:43.370626724Z [inf]  🎯 Hibrit Strateji başlatıldı: RESOLVUSDT (CRYPTO)
2025-10-17T22:08:43.370640753Z [inf]  🎯 Hibrit Strateji başlatıldı: KSMUSDT (CRYPTO)
2025-10-17T22:08:43.370660407Z [inf]  🎯 Hibrit Strateji başlatıldı: GIGGLEUSDT (CRYPTO)
2025-10-17T22:08:43.370667189Z [inf]  🎯 Hibrit Strateji başlatıldı: PHBUSDT (CRYPTO)
2025-10-17T22:08:43.370675694Z [inf]  🎯 Hibrit Strateji başlatıldı: NEWTUSDT (CRYPTO)
2025-10-17T22:08:43.370683807Z [inf]  🎯 Hibrit Strateji başlatıldı: OBOLUSDT (CRYPTO)
2025-10-17T22:08:43.370690376Z [inf]  🎯 Hibrit Strateji başlatıldı: ZILUSDT (CRYPTO)
2025-10-17T22:08:43.370696496Z [inf]  🎯 Hibrit Strateji başlatıldı: WAVESUSDT (CRYPTO)
2025-10-17T22:08:43.370703856Z [inf]  🎯 Hibrit Strateji başlatıldı: THEUSDT (CRYPTO)
2025-10-17T22:08:43.370713993Z [inf]  🎯 Hibrit Strateji başlatıldı: PIPEUSDT (CRYPTO)
2025-10-17T22:08:43.370721829Z [inf]  🎯 Hibrit Strateji başlatıldı: SKYAIUSDT (CRYPTO)
2025-10-17T22:08:43.370729498Z [inf]  🎯 Hibrit Strateji başlatıldı: MEUSDT (CRYPTO)
2025-10-17T22:08:43.370735902Z [inf]  🎯 Hibrit Strateji başlatıldı: PIXELUSDT (CRYPTO)
2025-10-17T22:08:43.370741948Z [inf]  🎯 Hibrit Strateji başlatıldı: ZENTUSDT (CRYPTO)
2025-10-17T22:08:43.370747947Z [inf]  🎯 Hibrit Strateji başlatıldı: SKLUSDT (CRYPTO)
2025-10-17T22:08:43.370756542Z [inf]  🎯 Hibrit Strateji başlatıldı: ZRCUSDT (CRYPTO)
2025-10-17T22:08:43.370763764Z [inf]  🎯 Hibrit Strateji başlatıldı: DOGSUSDT (CRYPTO)
2025-10-17T22:08:43.370770795Z [inf]  🎯 Hibrit Strateji başlatıldı: ZETAUSDT (CRYPTO)
2025-10-17T22:08:43.370776974Z [inf]  🎯 Hibrit Strateji başlatıldı: CWTUSDT (CRYPTO)
2025-10-17T22:08:43.370784398Z [inf]  🎯 Hibrit Strateji başlatıldı: WINUSDT (CRYPTO)
2025-10-17T22:08:43.370791073Z [inf]  🎯 Hibrit Strateji başlatıldı: TLMUSDT (CRYPTO)
2025-10-17T22:08:43.374464918Z [inf]  🎯 Hibrit Strateji başlatıldı: MUSDT (CRYPTO)
2025-10-17T22:08:43.374478181Z [inf]  🎯 Hibrit Strateji başlatıldı: ULTIMAUSDT (CRYPTO)
2025-10-17T22:08:43.374486400Z [inf]  🎯 Hibrit Strateji başlatıldı: PORTALUSDT (CRYPTO)
2025-10-17T22:08:43.374493510Z [inf]  🎯 Hibrit Strateji başlatıldı: QTUMUSDT (CRYPTO)
2025-10-17T22:08:43.374501325Z [inf]  🎯 Hibrit Strateji başlatıldı: NOMUSDT (CRYPTO)
2025-10-17T22:08:43.374509629Z [inf]  🎯 Hibrit Strateji başlatıldı: LQTYUSDT (CRYPTO)
2025-10-17T22:08:43.374516951Z [inf]  🎯 Hibrit Strateji başlatıldı: XVGUSDT (CRYPTO)
2025-10-17T22:08:43.374524643Z [inf]  🎯 Hibrit Strateji başlatıldı: NAORISUSDT (CRYPTO)
2025-10-17T22:08:43.374530701Z [inf]  🎯 Hibrit Strateji başlatıldı: BANKUSDT (CRYPTO)
2025-10-17T22:08:43.374538123Z [inf]  🎯 Hibrit Strateji başlatıldı: SAPIENUSDT (CRYPTO)
2025-10-17T22:08:43.374544582Z [inf]  🎯 Hibrit Strateji başlatıldı: DBRUSDT (CRYPTO)
2025-10-17T22:08:43.374551021Z [inf]  🎯 Hibrit Strateji başlatıldı: ATAUSDT (CRYPTO)
2025-10-17T22:08:43.374559667Z [inf]  🎯 Hibrit Strateji başlatıldı: UCNUSDT (CRYPTO)
2025-10-17T22:08:43.374565983Z [inf]  🎯 Hibrit Strateji başlatıldı: EPICUSDT (CRYPTO)
2025-10-17T22:08:43.374573368Z [inf]  🎯 Hibrit Strateji başlatıldı: BANUSDT (CRYPTO)
2025-10-17T22:08:43.374579880Z [inf]  🎯 Hibrit Strateji başlatıldı: PHAUSDT (CRYPTO)
2025-10-17T22:08:43.374586588Z [inf]  🎯 Hibrit Strateji başlatıldı: ELXUSDT (CRYPTO)
2025-10-17T22:08:43.374594002Z [inf]  🎯 Hibrit Strateji başlatıldı: SXTUSDT (CRYPTO)
2025-10-17T22:08:43.374603305Z [inf]  🎯 Hibrit Strateji başlatıldı: PROUSDT (CRYPTO)
2025-10-17T22:08:43.374609564Z [inf]  🎯 Hibrit Strateji başlatıldı: UBUSDT (CRYPTO)
2025-10-17T22:08:43.374615557Z [inf]  🎯 Hibrit Strateji başlatıldı: ETHWUSDT (CRYPTO)
2025-10-17T22:08:43.377996235Z [inf]  🎯 Hibrit Strateji başlatıldı: FLOWUSDT (CRYPTO)
2025-10-17T22:08:43.378007900Z [inf]  🎯 Hibrit Strateji başlatıldı: ROAMUSDT (CRYPTO)
2025-10-17T22:08:43.378014555Z [inf]  🎯 Hibrit Strateji başlatıldı: TSTUSDT (CRYPTO)
2025-10-17T22:08:43.378022265Z [inf]  🎯 Hibrit Strateji başlatıldı: BABYDOGEUSDT (CRYPTO)
2025-10-17T22:08:43.378028543Z [inf]  🎯 Hibrit Strateji başlatıldı: AAPLXUSDT (CRYPTO)
2025-10-17T22:08:43.378042156Z [inf]  🎯 Hibrit Strateji başlatıldı: CUDISUSDT (CRYPTO)
2025-10-17T22:08:43.378049959Z [inf]  🎯 Hibrit Strateji başlatıldı: FUNUSDT (CRYPTO)
2025-10-17T22:08:43.378055103Z [inf]  🎯 Hibrit Strateji başlatıldı: MXUSDT (CRYPTO)
2025-10-17T22:08:43.378061377Z [inf]  🎯 Hibrit Strateji başlatıldı: WSTUSDTUSDT (CRYPTO)
2025-10-17T22:08:43.378066706Z [inf]  🎯 Hibrit Strateji başlatıldı: HIPPOUSDT (CRYPTO)
2025-10-17T22:08:43.378071598Z [inf]  🎯 Hibrit Strateji başlatıldı: PSTAKEUSDT (CRYPTO)
2025-10-17T22:08:43.378076689Z [inf]  🎯 Hibrit Strateji başlatıldı: EGL1USDT (CRYPTO)
2025-10-17T22:08:43.378083688Z [inf]  🎯 Hibrit Strateji başlatıldı: FLUIDUSDT (CRYPTO)
2025-10-17T22:08:43.378088058Z [inf]  🎯 Hibrit Strateji başlatıldı: FHEUSDT (CRYPTO)
2025-10-17T22:08:43.378092646Z [inf]  🎯 Hibrit Strateji başlatıldı: XCNUSDT (CRYPTO)
2025-10-17T22:08:43.378098265Z [inf]  🎯 Hibrit Strateji başlatıldı: BMTUSDT (CRYPTO)
2025-10-17T22:08:43.378104771Z [inf]  🎯 Hibrit Strateji başlatıldı: SATSUSDT (CRYPTO)
2025-10-17T22:08:43.378110322Z [inf]  🎯 Hibrit Strateji başlatıldı: PUSDT (CRYPTO)
2025-10-17T22:08:43.378130475Z [inf]  🎯 Hibrit Strateji başlatıldı: MOMOUSDT (CRYPTO)
2025-10-17T22:08:43.378137606Z [inf]  🎯 Hibrit Strateji başlatıldı: TRUUSDT (CRYPTO)
2025-10-17T22:08:43.381203115Z [inf]  🎯 Hibrit Strateji başlatıldı: MFUSDT (CRYPTO)
2025-10-17T22:08:43.381217452Z [inf]  🎯 Hibrit Strateji başlatıldı: SCRUSDT (CRYPTO)
2025-10-17T22:08:43.381225798Z [inf]  🎯 Hibrit Strateji başlatıldı: GOMININGUSDT (CRYPTO)
2025-10-17T22:08:43.381227127Z [inf]  🎯 Hibrit Strateji başlatıldı: GLMUSDT (CRYPTO)
2025-10-17T22:08:43.381234068Z [inf]  🎯 Hibrit Strateji başlatıldı: SAGAUSDT (CRYPTO)
2025-10-17T22:08:43.381241052Z [inf]  🎯 Hibrit Strateji başlatıldı: AIOZUSDT (CRYPTO)
2025-10-17T22:08:43.381242754Z [inf]  🎯 Hibrit Strateji başlatıldı: KNCUSDT (CRYPTO)
2025-10-17T22:08:43.381249078Z [inf]  🎯 Hibrit Strateji başlatıldı: WXTUSDT (CRYPTO)
2025-10-17T22:08:43.381252528Z [inf]  🎯 Hibrit Strateji başlatıldı: BANDUSDT (CRYPTO)
2025-10-17T22:08:43.381258546Z [inf]  🎯 Hibrit Strateji başlatıldı: TAIKOUSDT (CRYPTO)
2025-10-17T22:08:43.381264663Z [inf]  🎯 Hibrit Strateji başlatıldı: DEEPUSDT (CRYPTO)
2025-10-17T22:08:43.381268419Z [inf]  🎯 Hibrit Strateji başlatıldı: AIDOGEUSDT (CRYPTO)
2025-10-17T22:08:43.381275706Z [inf]  🎯 Hibrit Strateji başlatıldı: SIGNUSDT (CRYPTO)
2025-10-17T22:08:43.381282452Z [inf]  🎯 Hibrit Strateji başlatıldı: PONKEUSDT (CRYPTO)
2025-10-17T22:08:43.381287999Z [inf]  🎯 Hibrit Strateji başlatıldı: GNOUSDT (CRYPTO)
2025-10-17T22:08:43.381297283Z [inf]  🎯 Hibrit Strateji başlatıldı: HEMIUSDT (CRYPTO)
2025-10-17T22:08:43.381305610Z [inf]  🎯 Hibrit Strateji başlatıldı: AIAUSDT (CRYPTO)
2025-10-17T22:08:43.381313442Z [inf]  🎯 Hibrit Strateji başlatıldı: LRCUSDT (CRYPTO)
2025-10-17T22:08:43.381320832Z [inf]  🎯 Hibrit Strateji başlatıldı: LYNUSDT (CRYPTO)
2025-10-17T22:08:43.381330146Z [inf]  🎯 Hibrit Strateji başlatıldı: AUCTIONUSDT (CRYPTO)
2025-10-17T22:08:43.384223376Z [inf]  🎯 Hibrit Strateji başlatıldı: PAALUSDT (CRYPTO)
2025-10-17T22:08:43.384224134Z [inf]  ✓ Scanner started in background thread.
2025-10-17T22:08:43.384234007Z [err]  INFO:     Application startup complete.
2025-10-17T22:08:43.384234216Z [inf]  🎯 Hibrit Strateji başlatıldı: L3USDT (CRYPTO)
2025-10-17T22:08:43.384242259Z [inf]  🎯 Hibrit Strateji başlatıldı: TAGUSDT (CRYPTO)
2025-10-17T22:08:43.384243026Z [err]  INFO:     Uvicorn running on http://0.0.0.0:8080 (Press CTRL+C to quit)
2025-10-17T22:08:43.384250413Z [inf]  🎯 Hibrit Strateji başlatıldı: DUSDT (CRYPTO)
2025-10-17T22:08:43.384257585Z [inf]  🎯 Hibrit Strateji başlatıldı: ONTUSDT (CRYPTO)
2025-10-17T22:08:43.384259583Z [inf]  🎯 Hibrit Strateji başlatıldı: ALPINEUSDT (CRYPTO)
2025-10-17T22:08:43.384266094Z [inf]  🎯 Hibrit Strateji başlatıldı: NFPUSDT (CRYPTO)
2025-10-17T22:08:43.384268168Z [inf]  🎯 Hibrit Strateji başlatıldı: EURQUSDT (CRYPTO)
2025-10-17T22:08:43.384274301Z [inf]  🎯 Hibrit Strateji başlatıldı: UNIFIUSDT (CRYPTO)
2025-10-17T22:08:43.384275753Z [inf]  🎯 Hibrit Strateji başlatıldı: PINGPONGUSDT (CRYPTO)
2025-10-17T22:08:43.384282554Z [inf]  🎯 Hibrit Strateji başlatıldı: JYAIUSDT (CRYPTO)
2025-10-17T22:08:43.384282686Z [inf]  🎯 Hibrit Strateji başlatıldı: XTERUSDT (CRYPTO)
2025-10-17T22:08:43.384290162Z [inf]  ✓ Stratejiler hazırlandı
2025-10-17T22:08:43.384296707Z [inf]  ======================================================================
2025-10-17T22:08:43.384304175Z [inf]  
2025-10-17T22:08:43.384310137Z [inf]  
2025-10-17T22:08:43.384316330Z [inf]  [2025-10-17 22:08:42 UTC] Tarama başladı...
2025-10-17T22:08:44.268651948Z [inf]  INFO:     100.64.0.2:33699 - "GET /health HTTP/1.1" 200 OK
2025-10-17T22:08:46.392138236Z [inf]  ❌ BTCUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:08:46.392144290Z [inf]  ⚠️ BTCUSDT hatası: 'RSI'...
2025-10-17T22:08:47.272916488Z [inf]  ❌ ETHUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:08:47.272923300Z [inf]  ⚠️ ETHUSDT hatası: 'RSI'...
2025-10-17T22:08:47.272930635Z [inf]  ❌ SOLUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:08:47.272937128Z [inf]  ⚠️ SOLUSDT hatası: 'RSI'...
2025-10-17T22:08:47.272944337Z [inf]  ❌ BNBUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:08:47.424770875Z [inf]  ❌ USDCUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:08:48.209515501Z [inf]  ❌ DOGEUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:08:48.368135728Z [inf]  ❌ XRPUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:08:48.636145682Z [inf]  ❌ 2ZUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:08:49.251237588Z [inf]  ❌ TRXUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:08:49.251243369Z [inf]  ❌ ADAUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:08:49.402370286Z [inf]  ❌ PEPEUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:08:50.196984841Z [inf]  ❌ SUIUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:08:50.196989184Z [inf]  ❌ ASTERUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:08:50.196994278Z [inf]  ❌ OKB/USDT veri çekme hatası: binance does not have market symbol OKB/USDT
2025-10-17T22:08:50.206852631Z [inf]  ❌ ENAUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:08:50.463359251Z [inf]  ❌ XPLUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:08:51.329216163Z [inf]  ❌ AVAXUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:08:51.397891889Z [inf]  ❌ LINKUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:08:51.655578594Z [inf]  ❌ LTCUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:08:52.350175135Z [inf]  ❌ AAVEUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:08:52.613013813Z [inf]  ❌ FDUSDUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:08:52.638734720Z [inf]  ❌ MNT/USDT veri çekme hatası: binance does not have market symbol MNT/USDT
2025-10-17T22:08:52.669738738Z [inf]  ❌ XAUT/USDT veri çekme hatası: binance does not have market symbol XAUT/USDT
2025-10-17T22:08:53.295159804Z [inf]  ❌ ZECUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:08:53.295175395Z [inf]  ❌ HYPE/USDT veri çekme hatası: binance does not have market symbol HYPE/USDT
2025-10-17T22:08:53.295184886Z [inf]  ❌ USDEUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:08:54.326125814Z [inf]  ❌ WIFUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:08:54.326132967Z [inf]  ❌ PAXGUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:08:54.402921144Z [inf]  ❌ YBUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:08:54.658283995Z [inf]  ❌ APTUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:08:55.296465053Z [inf]  ❌ TRUMPUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:08:55.296479649Z [inf]  ❌ TAOUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:08:55.431143613Z [inf]  ❌ ARBUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:08:55.696281813Z [inf]  ❌ DOTUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:08:56.301545567Z [inf]  ❌ UNIUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:08:56.301552295Z [inf]  ❌ NEARUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:08:56.531651847Z [inf]  ❌ CAKEUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:08:56.563368492Z [inf]  ❌ KGEN/USDT veri çekme hatası: binance does not have market symbol KGEN/USDT
2025-10-17T22:08:56.617299281Z [inf]  ❌ BLESS/USDT veri çekme hatası: binance does not have market symbol BLESS/USDT
2025-10-17T22:08:57.302660074Z [inf]  ❌ BCHUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:08:57.550068815Z [inf]  ❌ XLMUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:08:58.354582598Z [inf]  ❌ BGB/USDT veri çekme hatası: binance does not have market symbol BGB/USDT
2025-10-17T22:08:58.354673690Z [inf]  ❌ PENGUUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:08:58.354682776Z [inf]  ❌ BONKUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:08:58.361104554Z [inf]  ❌ BELUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:08:58.620389850Z [inf]  ❌ HBARUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:08:59.393563526Z [inf]  ❌ CRVUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:08:59.393573227Z [inf]  ❌ UGOLD/USDT veri çekme hatası: binance does not have market symbol UGOLD/USDT
2025-10-17T22:08:59.393580729Z [inf]  ❌ COAI/USDT veri çekme hatası: binance does not have market symbol COAI/USDT
2025-10-17T22:08:59.393586503Z [inf]  ❌ PUMPUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:08:59.450883248Z [inf]  ❌ WLFIUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:08:59.706796717Z [inf]  ❌ TONUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:00.591461117Z [inf]  ❌ LDOUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:00.591473674Z [inf]  ❌ SNXUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:00.591553287Z [inf]  ❌ WLDUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:00.742066508Z [inf]  ❌ XMRUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:01.350408377Z [inf]  ❌ ONDOUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:01.350415429Z [inf]  ❌ ETCUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:01.508465989Z [inf]  ❌ SHIBUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:02.479697848Z [inf]  ❌ DASHUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:02.479704932Z [inf]  ❌ FILUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:02.479842749Z [inf]  ❌ SEIUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:02.546031587Z [inf]  ❌ OPUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:03.324438379Z [inf]  ❌ YGGUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:03.324453227Z [inf]  ❌ FETUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:03.324462372Z [inf]  ❌ FORMUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:03.573402906Z [inf]  ❌ PENDLEUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:03.597505246Z [inf]  ❌ FARTCOIN/USDT veri çekme hatası: binance does not have market symbol FARTCOIN/USDT
2025-10-17T22:09:04.445800519Z [inf]  ❌ DEGOUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:04.445809268Z [inf]  ❌ SUSDE/USDT veri çekme hatası: binance does not have market symbol SUSDE/USDT
2025-10-17T22:09:04.576212468Z [inf]  ❌ EIGENUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:05.432745323Z [inf]  ❌ ENSOUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:05.432750933Z [inf]  ❌ FLOKIUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:05.432756554Z [inf]  ❌ TA/USDT veri çekme hatası: binance does not have market symbol TA/USDT
2025-10-17T22:09:05.432762053Z [inf]  ❌ RECALL/USDT veri çekme hatası: binance does not have market symbol RECALL/USDT
2025-10-17T22:09:05.432766823Z [inf]  ❌ SOON/USDT veri çekme hatası: binance does not have market symbol SOON/USDT
2025-10-17T22:09:05.443109701Z [inf]  ❌ LINEAUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:05.482037903Z [inf]  ❌ IP/USDT veri çekme hatası: binance does not have market symbol IP/USDT
2025-10-17T22:09:05.510021926Z [inf]  ❌ H/USDT veri çekme hatası: binance does not have market symbol H/USDT
2025-10-17T22:09:06.328715561Z [inf]  ❌ SUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:06.328721781Z [inf]  ❌ POLUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:06.328730934Z [inf]  ❌ ZORA/USDT veri çekme hatası: binance does not have market symbol ZORA/USDT
2025-10-17T22:09:06.328736480Z [inf]  ❌ FFUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:06.561029531Z [inf]  ❌ VIRTUALUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:07.355504183Z [inf]  ❌ SUPERUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:07.355510797Z [inf]  ❌ GALAUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:07.355517069Z [inf]  ❌ ATOMUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:07.594695650Z [inf]  ❌ USD1USDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:08.435685674Z [inf]  ❌ TIAUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:08.435696569Z [inf]  ❌ ALGOUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:08.435738864Z [inf]  ❌ WUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:08.623796067Z [inf]  ❌ WALUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:08.665266748Z [inf]  ❌ WBT/USDT veri çekme hatası: binance does not have market symbol WBT/USDT
2025-10-17T22:09:09.362398509Z [inf]  ❌ WBTCUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:09.362462089Z [inf]  ❌ INJUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:09.417491983Z [inf]  ❌ OMUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:09.445540260Z [inf]  ❌ KAS/USDT veri çekme hatası: binance does not have market symbol KAS/USDT
2025-10-17T22:09:09.707831232Z [inf]  ❌ ICPUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:10.383750020Z [inf]  ❌ ETHFIUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:10.383756826Z [inf]  ❌ USELESS/USDT veri çekme hatası: binance does not have market symbol USELESS/USDT
2025-10-17T22:09:10.383762834Z [inf]  ❌ RENDERUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:10.502576999Z [inf]  ❌ DAIUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:10.535530838Z [inf]  ❌ ATH/USDT veri çekme hatası: binance does not have market symbol ATH/USDT
2025-10-17T22:09:11.361432241Z [inf]  ❌ PNUTUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:11.361444228Z [inf]  ❌ MORPHOUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:11.361450335Z [inf]  ❌ RSRUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:11.553983540Z [inf]  ❌ BATUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:12.350204831Z [inf]  ❌ ALICEUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:12.350209127Z [inf]  ❌ PROVEUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:12.350213552Z [inf]  ❌ LAUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:12.588472462Z [inf]  ❌ TWTUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:12.619595765Z [inf]  ❌ STETH/USDT veri çekme hatası: binance does not have market symbol STETH/USDT
2025-10-17T22:09:12.638982922Z [inf]  ❌ B/USDT veri çekme hatası: binance does not have market symbol B/USDT
2025-10-17T22:09:13.450596135Z [inf]  ❌ IMXUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:13.450605658Z [inf]  ❌ ENSUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:13.450615866Z [inf]  ❌ WCTUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:13.666073731Z [inf]  ❌ RDNTUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:13.694333828Z [inf]  ❌ A/USDT/USDT veri çekme hatası: binance does not have market symbol A/USDT/USDT
2025-10-17T22:09:14.546708723Z [inf]  ❌ ARPAUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:14.546715425Z [inf]  ❌ ZENUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:14.546723910Z [inf]  ❌ LAB/USDT veri çekme hatası: binance does not have market symbol LAB/USDT
2025-10-17T22:09:14.546732893Z [inf]  ❌ HEIUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:14.750102254Z [inf]  ❌ SYRUPUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:15.364020494Z [inf]  ❌ BERAUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:15.364025846Z [inf]  ❌ HOOKUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:15.525084976Z [inf]  ❌ ARKMUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:15.780430536Z [inf]  ❌ OGUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:16.320784784Z [inf]  ❌ BRETT/USDT veri çekme hatası: binance does not have market symbol BRETT/USDT
2025-10-17T22:09:16.320797543Z [inf]  ❌ RAYUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:16.320936045Z [inf]  ❌ LAUNCHCO.../USDT veri çekme hatası: binance does not have market symbol LAUNCHCO.../USDT
2025-10-17T22:09:16.370225086Z [inf]  ❌ STRKUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:16.398996157Z [inf]  ❌ MYX/USDT veri çekme hatası: binance does not have market symbol MYX/USDT
2025-10-17T22:09:16.663357377Z [inf]  ❌ ORDIUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:17.438086180Z [inf]  ❌ BBUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:17.438095941Z [inf]  ❌ B2/USDT veri çekme hatası: binance does not have market symbol B2/USDT
2025-10-17T22:09:17.438199074Z [inf]  ❌ AXSUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:17.453645893Z [inf]  ❌ EDUUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:17.486620805Z [inf]  ❌ XDC/USDT veri çekme hatası: binance does not have market symbol XDC/USDT
2025-10-17T22:09:17.742130214Z [inf]  ❌ OPENUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:18.379747245Z [inf]  ❌ AVNTUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:18.379759013Z [inf]  ❌ SANDUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:18.511875983Z [inf]  ❌ SUNUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:18.767848030Z [inf]  ❌ ZROUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:19.316901773Z [inf]  ❌ APEUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:19.316909961Z [inf]  ❌ VETUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:19.557832645Z [inf]  ❌ PEOPLEUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:20.418835985Z [inf]  ❌ JSTUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:20.418842251Z [inf]  ❌ 0GUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:20.418849023Z [inf]  ❌ AUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:20.584519344Z [inf]  ❌ BIOUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:20.615507532Z [inf]  ❌ GRASS/USDT veri çekme hatası: binance does not have market symbol GRASS/USDT
2025-10-17T22:09:21.388467465Z [inf]  ❌ AIUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:21.388501697Z [inf]  ❌ PYTHUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:21.393928756Z [inf]  ❌ SPKUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:21.660929137Z [inf]  ❌ NEIROUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:21.682280047Z [inf]  ❌ AI16Z/USDT veri çekme hatası: binance does not have market symbol AI16Z/USDT
2025-10-17T22:09:22.533732564Z [inf]  ❌ COMPUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:22.533740468Z [inf]  ❌ JTOUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:22.533749917Z [inf]  ❌ USDR/USDT veri çekme hatası: binance does not have market symbol USDR/USDT
2025-10-17T22:09:22.533757506Z [inf]  ❌ BARDUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:22.735182344Z [inf]  ❌ SUSHIUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:23.471200395Z [inf]  ❌ CATIUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:23.471206979Z [inf]  ❌ HOLOUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:23.501014670Z [inf]  ❌ SOLVUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:24.594854754Z [inf]  ❌ MANAUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:24.594880199Z [inf]  ❌ ZKCUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:24.711072939Z [inf]  ❌ XUSDUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:24.747700220Z [inf]  ❌ CLO/USDT veri çekme hatası: binance does not have market symbol CLO/USDT
2025-10-17T22:09:24.781705636Z [inf]  ❌ XPIN/USDT veri çekme hatası: binance does not have market symbol XPIN/USDT
2025-10-17T22:09:25.458492318Z [inf]  ❌ JUPUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:25.458506717Z [inf]  ❌ POPCAT/USDT veri çekme hatası: binance does not have market symbol POPCAT/USDT
2025-10-17T22:09:25.458519102Z [inf]  ❌ PLUMEUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:25.604885121Z [inf]  ❌ ARUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:25.689985001Z [inf]  INFO:     100.64.0.3:22232 - "GET /api/signals?limit=50 HTTP/1.1" 200 OK
2025-10-17T22:09:25.725288246Z [inf]  INFO:     100.64.0.3:22248 - "GET /api/signals/stats HTTP/1.1" 200 OK
2025-10-17T22:09:25.728526984Z [inf]  INFO:     100.64.0.3:22258 - "GET /api/markets HTTP/1.1" 200 OK
2025-10-17T22:09:25.765125183Z [inf]  INFO:     100.64.0.3:22264 - "GET /api/trades/open HTTP/1.1" 200 OK
2025-10-17T22:09:25.765131202Z [inf]  INFO:     100.64.0.3:22268 - "GET /health HTTP/1.1" 200 OK
2025-10-17T22:09:25.805486798Z [inf]  Portfolio state error: {'message': "Could not find the table 'public.portfolio_state' in the schema cache", 'code': 'PGRST205', 'hint': None, 'details': None}
2025-10-17T22:09:25.805493908Z [inf]  INFO:     100.64.0.3:22276 - "GET /api/portfolio HTTP/1.1" 200 OK
2025-10-17T22:09:26.403391511Z [inf]  ❌ TUTUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:26.403403259Z [inf]  ❌ AB/USDT veri çekme hatası: binance does not have market symbol AB/USDT
2025-10-17T22:09:26.403410055Z [inf]  ❌ BOMEUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:26.403547614Z [inf]  INFO:     100.64.0.3:22274 - "GET /api/trades/closed HTTP/1.1" 200 OK
2025-10-17T22:09:26.411112169Z [inf]  ❌ KAIAUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:26.669962339Z [inf]  ❌ RUNEUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:27.469677491Z [inf]  ❌ KERNELUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:27.469683910Z [inf]  ❌ PI/USDT veri çekme hatası: binance does not have market symbol PI/USDT
2025-10-17T22:09:27.469690736Z [inf]  ❌ TURBOUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:27.484362052Z [inf]  ❌ LUNAUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:27.741250044Z [inf]  ❌ CYBERUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:28.490935797Z [inf]  ❌ STOUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:28.490942966Z [inf]  ❌ 1INCHUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:28.520648933Z [inf]  ❌ CHZUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:28.553051983Z [inf]  ❌ 4/USDT veri çekme hatası: binance does not have market symbol 4/USDT
2025-10-17T22:09:28.824785952Z [inf]  ❌ IOUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:29.452009592Z [inf]  ❌ ALCH/USDT veri çekme hatası: binance does not have market symbol ALCH/USDT
2025-10-17T22:09:29.452023038Z [inf]  ❌ GMTUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:29.452140781Z [inf]  ❌ GRTUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:29.639716902Z [inf]  ❌ NMRUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:29.682783905Z [inf]  ❌ XAN/USDT veri çekme hatası: binance does not have market symbol XAN/USDT
2025-10-17T22:09:30.436963964Z [inf]  ❌ MBG/USDT veri çekme hatası: binance does not have market symbol MBG/USDT
2025-10-17T22:09:30.436978901Z [inf]  ❌ MOODENG/USDT veri çekme hatası: binance does not have market symbol MOODENG/USDT
2025-10-17T22:09:30.437080952Z [inf]  ❌ MIRAUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:30.437090920Z [inf]  ❌ CFXUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:30.535912659Z [inf]  ❌ JASMYUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:30.801349992Z [inf]  ❌ HOMEUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:30.801360218Z [inf]  INFO:     100.64.0.3:22274 - "GET /health HTTP/1.1" 200 OK
2025-10-17T22:09:31.503840402Z [inf]  ❌ REDUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:31.503847878Z [inf]  ❌ ARIA/USDT veri çekme hatası: binance does not have market symbol ARIA/USDT
2025-10-17T22:09:31.503856423Z [inf]  ❌ MAGICUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:31.503866211Z [inf]  ❌ MEW/USDT veri çekme hatası: binance does not have market symbol MEW/USDT
2025-10-17T22:09:31.503875523Z [inf]  ❌ VRA/USDT veri çekme hatası: binance does not have market symbol VRA/USDT
2025-10-17T22:09:31.680789641Z [inf]  ❌ MEMEUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:32.486668851Z [inf]  ❌ BAS/USDT veri çekme hatası: binance does not have market symbol BAS/USDT
2025-10-17T22:09:32.486690127Z [inf]  ❌ ETHDYDX/USDT veri çekme hatası: binance does not have market symbol ETHDYDX/USDT
2025-10-17T22:09:32.486698210Z [inf]  ❌ YFIUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:32.486736898Z [inf]  ❌ MASKUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:32.486747350Z [inf]  ❌ DRIFT/USDT veri çekme hatası: binance does not have market symbol DRIFT/USDT
2025-10-17T22:09:32.557073370Z [inf]  ❌ ANIMEUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:32.815935609Z [inf]  ❌ ACTUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:32.848879000Z [inf]  ❌ ZBCN/USDT veri çekme hatası: binance does not have market symbol ZBCN/USDT
2025-10-17T22:09:33.391769106Z [inf]  ❌ SHELLUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:33.391777920Z [inf]  ❌ ZKUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:33.640030791Z [inf]  ❌ SOMIUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:34.592676639Z [inf]  ❌ AEVOUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:34.592683754Z [inf]  ❌ APEX/USDT veri çekme hatası: binance does not have market symbol APEX/USDT
2025-10-17T22:09:34.592690297Z [inf]  ❌ MOVEUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:34.592696380Z [inf]  ❌ STEEMUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:34.592702497Z [inf]  ❌ REAL/USDT veri çekme hatası: binance does not have market symbol REAL/USDT
2025-10-17T22:09:34.745179806Z [inf]  ❌ THETAUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:34.781521378Z [inf]  ❌ PTB/USDT veri çekme hatası: binance does not have market symbol PTB/USDT
2025-10-17T22:09:34.820142684Z [inf]  ❌ MERL/USDT veri çekme hatası: binance does not have market symbol MERL/USDT
2025-10-17T22:09:34.847744687Z [inf]  ❌ K/USDT veri çekme hatası: binance does not have market symbol K/USDT
2025-10-17T22:09:35.506659805Z [inf]  ❌ TOSHI/USDT veri çekme hatası: binance does not have market symbol TOSHI/USDT
2025-10-17T22:09:35.506672732Z [inf]  ❌ STBL/USDT veri çekme hatası: binance does not have market symbol STBL/USDT
2025-10-17T22:09:35.506678503Z [inf]  ❌ ZEREBRO/USDT veri çekme hatası: binance does not have market symbol ZEREBRO/USDT
2025-10-17T22:09:35.506683812Z [inf]  ❌ PRCL/USDT veri çekme hatası: binance does not have market symbol PRCL/USDT
2025-10-17T22:09:35.506723216Z [inf]  ❌ INITUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:35.506727913Z [inf]  ❌ TRBUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:35.756704072Z [inf]  ❌ DEXEUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:35.792485346Z [inf]  ❌ F/USDT veri çekme hatası: binance does not have market symbol F/USDT
2025-10-17T22:09:35.826182244Z [inf]  ❌ RATS/USDT veri çekme hatası: binance does not have market symbol RATS/USDT
2025-10-17T22:09:36.464312252Z [inf]  ❌ HUMAUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:36.464317145Z [inf]  ❌ CRO/USDT veri çekme hatası: binance does not have market symbol CRO/USDT
2025-10-17T22:09:36.464323284Z [inf]  ❌ AMPUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:36.633515530Z [inf]  ❌ HAEDALUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:36.892649213Z [inf]  ❌ VANAUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:37.478204232Z [inf]  ❌ CHRUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:37.478215394Z [inf]  ❌ TREEUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:37.478279512Z [inf]  ❌ APEPE/USDT veri çekme hatası: binance does not have market symbol APEPE/USDT
2025-10-17T22:09:37.706095679Z [inf]  ❌ EDENUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:37.748901413Z [inf]  Attempting to close trade: ZENUSDT @ $12.452
2025-10-17T22:09:37.871134320Z [inf]  Found open trade: {'id': 11, 'symbol': 'ZENUSDT', 'trade_type': 'LONG', 'entry_price': 12.536, 'entry_time': '2025-10-16T12:45:47.095595+00:00', 'status': 'OPEN', 'created_at': '2025-10-16T12:45:47.119739+00:00', 'updated_at': '2025-10-16T12:45:47.119739+00:00', 'atr_value': 0.1765, 'stop_loss': 12.09475, 'take_profit': 13.85975, 'system': 'HYBRID_CRYPTO'}
2025-10-17T22:09:37.871143082Z [inf]  Closing LONG position: Entry $12.536, Exit $12.452
2025-10-17T22:09:37.871149665Z [inf]  Calculated P&L: -0.67% = $-1.68
2025-10-17T22:09:38.531045674Z [inf]  Error closing trade for ZENUSDT: {'message': "Could not find the 'leverage' column of 'closed_trades' in the schema cache", 'code': 'PGRST204', 'hint': None, 'details': None}
2025-10-17T22:09:38.531157121Z [inf]  INFO:     100.64.0.4:50348 - "POST /close-trade/ZENUSDT?exit_price=12.452 HTTP/1.1" 200 OK
2025-10-17T22:09:38.531172366Z [inf]  ❌ SAHARAUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:38.531178526Z [inf]  ❌ KAITOUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:38.531184744Z [inf]  ❌ SPX/USDT veri çekme hatası: binance does not have market symbol SPX/USDT
2025-10-17T22:09:38.531190989Z [inf]  ❌ WETH/USDT veri çekme hatası: binance does not have market symbol WETH/USDT
2025-10-17T22:09:38.571976061Z [inf]  ❌ QNTUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:38.832445975Z [inf]  ❌ EULUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:39.447513906Z [inf]  ❌ PARTIUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:39.447518394Z [inf]  ❌ SSVUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:39.617780299Z [inf]  ❌ USTCUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:39.656487952Z [inf]  ❌ AERO/USDT veri çekme hatası: binance does not have market symbol AERO/USDT
2025-10-17T22:09:40.528855772Z [inf]  ❌ NOTUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:40.528895392Z [inf]  ❌ ALTUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:40.528902779Z [inf]  ❌ AIXBTUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:40.689542256Z [inf]  ❌ RAREUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:40.724156322Z [inf]  ❌ XT/USDT veri çekme hatası: binance does not have market symbol XT/USDT
2025-10-17T22:09:41.517128941Z [inf]  ❌ API3USDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:41.517139643Z [inf]  ❌ DOOD/USDT veri çekme hatası: binance does not have market symbol DOOD/USDT
2025-10-17T22:09:41.517253803Z [inf]  ❌ STXUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:41.531654939Z [inf]  ❌ NEOUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:41.569235735Z [inf]  ❌ USDQ/USDT veri çekme hatası: binance does not have market symbol USDQ/USDT
2025-10-17T22:09:41.826318955Z [inf]  ❌ MBOXUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:41.865275700Z [inf]  ❌ SONIC/USDT veri çekme hatası: binance does not have market symbol SONIC/USDT
2025-10-17T22:09:42.552059436Z [inf]  ❌ LISTAUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:42.815507007Z [inf]  ❌ XTZUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:43.797807385Z [inf]  ❌ ILVUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:43.797813017Z [inf]  ❌ LUNCUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:43.797824651Z [inf]  ❌ FLK/USDT veri çekme hatası: binance does not have market symbol FLK/USDT
2025-10-17T22:09:43.797830501Z [inf]  ❌ CLANKER/USDT veri çekme hatası: binance does not have market symbol CLANKER/USDT
2025-10-17T22:09:43.797836400Z [inf]  ❌ SQD/USDT veri çekme hatası: binance does not have market symbol SQD/USDT
2025-10-17T22:09:43.797841834Z [inf]  ❌ VELO/USDT veri çekme hatası: binance does not have market symbol VELO/USDT
2025-10-17T22:09:44.672589875Z [inf]  ❌ AITECH/USDT veri çekme hatası: binance does not have market symbol AITECH/USDT
2025-10-17T22:09:44.672701316Z [inf]  ❌ CELOUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:44.672709552Z [inf]  ❌ NEXOUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:44.713096845Z [inf]  ❌ BTTUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:45.539519125Z [inf]  ❌ UMAUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:45.539527573Z [inf]  ❌ $MBG/USDT veri çekme hatası: binance does not have market symbol $MBG/USDT
2025-10-17T22:09:45.539535654Z [inf]  ❌ CVXUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:45.539542877Z [inf]  ❌ HYPERUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:45.555352630Z [inf]  ❌ VINE/USDT veri çekme hatası: binance does not have market symbol VINE/USDT
2025-10-17T22:09:45.584963047Z [inf]  ❌ FTN/USDT veri çekme hatası: binance does not have market symbol FTN/USDT
2025-10-17T22:09:45.845527691Z [inf]  ❌ REZUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:45.878645606Z [inf]  ❌ HANA/USDT veri çekme hatası: binance does not have market symbol HANA/USDT
2025-10-17T22:09:46.674225805Z [inf]  ❌ NXPCUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:46.674234948Z [inf]  ❌ CETUSUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:46.674242653Z [inf]  ❌ NILUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:46.933358616Z [inf]  ❌ BFUSDUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:47.554005204Z [inf]  ❌ DYDXUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:47.554011786Z [inf]  ❌ ACHUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:47.783646044Z [inf]  ❌ MINAUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:48.552613340Z [inf]  ❌ ERAUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:48.552621381Z [inf]  ❌ BSVUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:48.576830393Z [inf]  ❌ A2ZUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:48.839190204Z [inf]  ❌ EGLDUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:49.543927139Z [inf]  ❌ FTTUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:49.543935209Z [inf]  ❌ CARV/USDT veri çekme hatası: binance does not have market symbol CARV/USDT
2025-10-17T22:09:49.543942730Z [inf]  ❌ LPTUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:49.648382032Z [inf]  ❌ BEAMUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:49.682268835Z [inf]  ❌ AVL/USDT veri çekme hatası: binance does not have market symbol AVL/USDT
2025-10-17T22:09:49.718117693Z [inf]  ❌ ORDER/USDT veri çekme hatası: binance does not have market symbol ORDER/USDT
2025-10-17T22:09:50.570377371Z [inf]  ❌ IOTXUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:50.570386808Z [inf]  ❌ IDUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:50.570393786Z [inf]  ❌ ANKRUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:50.767186057Z [inf]  ❌ XAIUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:51.558051122Z [inf]  ❌ HFTUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:51.558278455Z [inf]  ❌ MUBARAKUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:51.558284583Z [inf]  ❌ PUFFER/USDT veri çekme hatası: binance does not have market symbol PUFFER/USDT
2025-10-17T22:09:51.584018043Z [inf]  ❌ BABYUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:51.622809981Z [inf]  ❌ ES/USDT veri çekme hatası: binance does not have market symbol ES/USDT
2025-10-17T22:09:51.656758756Z [inf]  ❌ MPRA/USDT veri çekme hatası: binance does not have market symbol MPRA/USDT
2025-10-17T22:09:51.907827407Z [inf]  ❌ TOWNSUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:52.494019510Z [inf]  ❌ SKYUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:52.494031397Z [inf]  ❌ B3/USDT veri çekme hatası: binance does not have market symbol B3/USDT
2025-10-17T22:09:52.494134235Z [inf]  ❌ ZRXUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:52.726784089Z [inf]  ❌ BLURUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:52.767004749Z [inf]  ❌ PROMPT/USDT veri çekme hatası: binance does not have market symbol PROMPT/USDT
2025-10-17T22:09:52.798426456Z [inf]  ❌ MOCA/USDT veri çekme hatası: binance does not have market symbol MOCA/USDT
2025-10-17T22:09:53.511147203Z [inf]  ❌ IKA/USDT veri çekme hatası: binance does not have market symbol IKA/USDT
2025-10-17T22:09:53.511158947Z [inf]  ❌ LAYERUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:53.511166466Z [inf]  ❌ XYO/USDT veri çekme hatası: binance does not have market symbol XYO/USDT
2025-10-17T22:09:53.511174476Z [inf]  ❌ IDOL/USDT veri çekme hatası: binance does not have market symbol IDOL/USDT
2025-10-17T22:09:53.511218748Z [inf]  ❌ AXLUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:53.686394054Z [inf]  ❌ KAVAUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:53.723825424Z [inf]  ❌ FRAX/USDT veri çekme hatası: binance does not have market symbol FRAX/USDT
2025-10-17T22:09:53.758146351Z [inf]  ❌ BROCCOLI/USDT veri çekme hatası: binance does not have market symbol BROCCOLI/USDT
2025-10-17T22:09:54.694537928Z [inf]  ❌ JELLYJEL.../USDT veri çekme hatası: binance does not have market symbol JELLYJEL.../USDT
2025-10-17T22:09:54.694547568Z [inf]  ❌ HTX/USDT veri çekme hatası: binance does not have market symbol HTX/USDT
2025-10-17T22:09:54.694553217Z [inf]  ❌ SUNDOG/USDT veri çekme hatası: binance does not have market symbol SUNDOG/USDT
2025-10-17T22:09:54.694559697Z [inf]  ❌ CTC/USDT veri çekme hatası: binance does not have market symbol CTC/USDT
2025-10-17T22:09:54.694619180Z [inf]  ❌ IOTAUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:54.852077617Z [inf]  ❌ ASTRUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:54.884759677Z [inf]  ❌ DEGEN/USDT veri çekme hatası: binance does not have market symbol DEGEN/USDT
2025-10-17T22:09:54.918220925Z [inf]  ❌ MOG/USDT veri çekme hatası: binance does not have market symbol MOG/USDT
2025-10-17T22:09:54.951928116Z [inf]  ❌ TSLAX/USDT veri çekme hatası: binance does not have market symbol TSLAX/USDT
2025-10-17T22:09:55.615054090Z [inf]  ❌ CORE/USDT veri çekme hatası: binance does not have market symbol CORE/USDT
2025-10-17T22:09:55.615059283Z [inf]  ❌ KMNOUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:55.615064249Z [inf]  ❌ COOKIEUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:55.615073043Z [inf]  ❌ SKATE/USDT veri çekme hatası: binance does not have market symbol SKATE/USDT
2025-10-17T22:09:55.615078955Z [inf]  ❌ RDAC/USDT veri çekme hatası: binance does not have market symbol RDAC/USDT
2025-10-17T22:09:55.615085833Z [inf]  ❌ NFT/USDT veri çekme hatası: binance does not have market symbol NFT/USDT
2025-10-17T22:09:55.639983392Z [inf]  ❌ GAIA/USDT veri çekme hatası: binance does not have market symbol GAIA/USDT
2025-10-17T22:09:55.910206346Z [inf]  ❌ CGPTUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:55.940936403Z [inf]  ❌ CRCLX/USDT veri çekme hatası: binance does not have market symbol CRCLX/USDT
2025-10-17T22:09:56.611722776Z [inf]  ❌ IOSTUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:56.611734693Z [inf]  ❌ SUSDS/USDT veri çekme hatası: binance does not have market symbol SUSDS/USDT
2025-10-17T22:09:56.611746112Z [inf]  ❌ USUALUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:56.611755153Z [inf]  ❌ XION/USDT veri çekme hatası: binance does not have market symbol XION/USDT
2025-10-17T22:09:56.611764760Z [inf]  ❌ GOAT/USDT veri çekme hatası: binance does not have market symbol GOAT/USDT
2025-10-17T22:09:56.822451217Z [inf]  ❌ WOOUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:57.443077747Z [inf]  ❌ C98USDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:57.443092130Z [inf]  ❌ ICE/USDT veri çekme hatası: binance does not have market symbol ICE/USDT
2025-10-17T22:09:57.443119346Z [inf]  ❌ BIGTIMEUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:57.632736601Z [inf]  ❌ AGLDUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:57.901700262Z [inf]  ❌ RESOLVUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:58.585318248Z [inf]  ❌ PHBUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:58.585491277Z [inf]  ❌ KSMUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:58.585498822Z [inf]  ❌ GIGGLE/USDT veri çekme hatası: binance does not have market symbol GIGGLE/USDT
2025-10-17T22:09:58.727918631Z [inf]  ❌ NEWTUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:58.747280828Z [inf]  ❌ OBOL/USDT veri çekme hatası: binance does not have market symbol OBOL/USDT
2025-10-17T22:09:59.552019473Z [inf]  ❌ ZILUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:59.552030822Z [inf]  ❌ WAVESUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:59.552040066Z [inf]  ❌ THEUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:09:59.578556427Z [inf]  ❌ PIPE/USDT veri çekme hatası: binance does not have market symbol PIPE/USDT
2025-10-17T22:09:59.615439391Z [inf]  ❌ SKYAI/USDT veri çekme hatası: binance does not have market symbol SKYAI/USDT
2025-10-17T22:09:59.870678613Z [inf]  ❌ MEUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:10:00.627292692Z [inf]  ❌ PIXELUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:10:00.627300540Z [inf]  ❌ ZENT/USDT veri çekme hatası: binance does not have market symbol ZENT/USDT
2025-10-17T22:10:00.627308842Z [inf]  ❌ SKLUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:10:00.627317381Z [inf]  ❌ ZRC/USDT veri çekme hatası: binance does not have market symbol ZRC/USDT
2025-10-17T22:10:00.781170782Z [inf]  ❌ DOGSUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:10:00.812811113Z [inf]  ❌ ZETA/USDT veri çekme hatası: binance does not have market symbol ZETA/USDT
2025-10-17T22:10:00.835908833Z [inf]  ❌ CWT/USDT veri çekme hatası: binance does not have market symbol CWT/USDT
2025-10-17T22:10:01.751131892Z [inf]  ❌ WINUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:10:02.603323317Z [inf]  ❌ TLMUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:10:02.603332257Z [inf]  ❌ M/USDT veri çekme hatası: binance does not have market symbol M/USDT
2025-10-17T22:10:02.603340623Z [inf]  ❌ ULTIMA/USDT veri çekme hatası: binance does not have market symbol ULTIMA/USDT
2025-10-17T22:10:02.603354787Z [inf]  ❌ PORTALUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:10:02.732044301Z [inf]  ❌ QTUMUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:10:03.625521993Z [inf]  ❌ NOMUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:10:03.625530359Z [inf]  ❌ LQTYUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:10:03.625531792Z [inf]  ❌ NAORIS/USDT veri çekme hatası: binance does not have market symbol NAORIS/USDT
2025-10-17T22:10:03.625538390Z [inf]  ❌ XVGUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:10:03.625539637Z [inf]  ❌ BANK/USDT veri çekme hatası: binance does not have market symbol BANK/USDT
2025-10-17T22:10:03.625543887Z [inf]  ❌ SAPIEN/USDT veri çekme hatası: binance does not have market symbol SAPIEN/USDT
2025-10-17T22:10:03.644754477Z [inf]  ❌ DBR/USDT veri çekme hatası: binance does not have market symbol DBR/USDT
2025-10-17T22:10:03.907115380Z [inf]  ❌ ATAUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:10:03.943522583Z [inf]  ❌ UCN/USDT veri çekme hatası: binance does not have market symbol UCN/USDT
2025-10-17T22:10:04.551326530Z [inf]  ❌ EPICUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:10:04.551333553Z [inf]  ❌ BAN/USDT veri çekme hatası: binance does not have market symbol BAN/USDT
2025-10-17T22:10:04.551340127Z [inf]  ❌ PHAUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:10:04.551346840Z [inf]  ❌ ELX/USDT veri çekme hatası: binance does not have market symbol ELX/USDT
2025-10-17T22:10:04.801725531Z [inf]  ❌ SXTUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:10:04.842664174Z [inf]  ❌ PRO/USDT veri çekme hatası: binance does not have market symbol PRO/USDT
2025-10-17T22:10:04.870549583Z [inf]  ❌ UB/USDT veri çekme hatası: binance does not have market symbol UB/USDT
2025-10-17T22:10:04.926605831Z [inf]  ❌ ETHW/USDT veri çekme hatası: binance does not have market symbol ETHW/USDT
2025-10-17T22:10:04.949000889Z [inf]  ❌ CUDIS/USDT veri çekme hatası: binance does not have market symbol CUDIS/USDT
2025-10-17T22:10:05.673221234Z [inf]  ❌ FUNUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:10:05.673225792Z [inf]  ❌ MX/USDT veri çekme hatası: binance does not have market symbol MX/USDT
2025-10-17T22:10:05.673230521Z [inf]  ❌ WST/USDT/USDT veri çekme hatası: binance does not have market symbol WST/USDT/USDT
2025-10-17T22:10:05.673235199Z [inf]  ❌ HIPPO/USDT veri çekme hatası: binance does not have market symbol HIPPO/USDT
2025-10-17T22:10:05.673239737Z [inf]  ❌ PSTAKE/USDT veri çekme hatası: binance does not have market symbol PSTAKE/USDT
2025-10-17T22:10:05.673244772Z [inf]  ❌ EGL1/USDT veri çekme hatası: binance does not have market symbol EGL1/USDT
2025-10-17T22:10:05.673251174Z [inf]  ❌ FLUID/USDT veri çekme hatası: binance does not have market symbol FLUID/USDT
2025-10-17T22:10:05.673256154Z [inf]  ❌ FHE/USDT veri çekme hatası: binance does not have market symbol FHE/USDT
2025-10-17T22:10:05.673260721Z [inf]  ❌ XCN/USDT veri çekme hatası: binance does not have market symbol XCN/USDT
2025-10-17T22:10:05.755208651Z [inf]  ❌ BMTUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:10:05.789656132Z [inf]  ❌ SATS/USDT veri çekme hatası: binance does not have market symbol SATS/USDT
2025-10-17T22:10:05.840343382Z [inf]  ❌ P/USDT veri çekme hatası: binance does not have market symbol P/USDT
2025-10-17T22:10:05.856606576Z [inf]  ❌ MOMO/USDT veri çekme hatası: binance does not have market symbol MOMO/USDT
2025-10-17T22:10:06.707822772Z [inf]  ❌ FLOWUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:10:06.707831928Z [inf]  ❌ ROAM/USDT veri çekme hatası: binance does not have market symbol ROAM/USDT
2025-10-17T22:10:06.707847834Z [inf]  ❌ TSTUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:10:06.708048343Z [inf]  ❌ TRUUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:10:06.723798008Z [inf]  ❌ BABYDOGE/USDT veri çekme hatası: binance does not have market symbol BABYDOGE/USDT
2025-10-17T22:10:06.760841554Z [inf]  ❌ AAPLX/USDT veri çekme hatası: binance does not have market symbol AAPLX/USDT
2025-10-17T22:10:07.711125416Z [inf]  ❌ SCRUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:10:07.711132372Z [inf]  ❌ GOMINING/USDT veri çekme hatası: binance does not have market symbol GOMINING/USDT
2025-10-17T22:10:07.711141067Z [inf]  ❌ SAGAUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:10:07.711149060Z [inf]  ❌ KNCUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:10:07.863261590Z [inf]  ❌ BANDUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:10:07.894378337Z [inf]  ❌ DEEP/USDT veri çekme hatası: binance does not have market symbol DEEP/USDT
2025-10-17T22:10:08.685998086Z [inf]  ❌ TAIKO/USDT veri çekme hatası: binance does not have market symbol TAIKO/USDT
2025-10-17T22:10:08.686006715Z [inf]  ❌ AIDOGE/USDT veri çekme hatası: binance does not have market symbol AIDOGE/USDT
2025-10-17T22:10:08.686013535Z [inf]  ❌ SIGNUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:10:08.686019622Z [inf]  ❌ PONKE/USDT veri çekme hatası: binance does not have market symbol PONKE/USDT
2025-10-17T22:10:08.686088342Z [inf]  ❌ GLMUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:10:08.686095120Z [inf]  ❌ AIOZ/USDT veri çekme hatası: binance does not have market symbol AIOZ/USDT
2025-10-17T22:10:08.686101494Z [inf]  ❌ WXT/USDT veri çekme hatası: binance does not have market symbol WXT/USDT
2025-10-17T22:10:08.859502517Z [inf]  ❌ GNOUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:10:09.619833834Z [inf]  ❌ HEMIUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:10:09.619845961Z [inf]  ❌ AIA/USDT veri çekme hatası: binance does not have market symbol AIA/USDT
2025-10-17T22:10:09.619853849Z [inf]  ❌ LRCUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:10:09.619861034Z [inf]  ❌ LYN/USDT veri çekme hatası: binance does not have market symbol LYN/USDT
2025-10-17T22:10:09.714079658Z [inf]  ❌ AUCTIONUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:10:09.748257711Z [inf]  ❌ MF/USDT veri çekme hatası: binance does not have market symbol MF/USDT
2025-10-17T22:10:09.781594823Z [inf]  ❌ PAAL/USDT veri çekme hatası: binance does not have market symbol PAAL/USDT
2025-10-17T22:10:09.815890259Z [inf]  ❌ L3/USDT veri çekme hatası: binance does not have market symbol L3/USDT
2025-10-17T22:10:09.855310016Z [inf]  ❌ TAG/USDT veri çekme hatası: binance does not have market symbol TAG/USDT
2025-10-17T22:10:10.700057945Z [inf]  ❌ DUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:10:10.700064822Z [inf]  ❌ ONTUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:10:10.700071392Z [inf]  ❌ NFPUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:10:10.700081183Z [inf]  ❌ UNIFI/USDT veri çekme hatası: binance does not have market symbol UNIFI/USDT
2025-10-17T22:10:10.703349473Z [inf]  ❌ JYAI/USDT veri çekme hatası: binance does not have market symbol JYAI/USDT
2025-10-17T22:10:10.961191030Z [inf]  ❌ ALPINEUSDT gösterge hesaplama hatası: 'High'
2025-10-17T22:10:11.001004556Z [inf]  ❌ EURQ/USDT veri çekme hatası: binance does not have market symbol EURQ/USDT
2025-10-17T22:10:11.032391478Z [inf]  ❌ PINGPONG/USDT veri çekme hatası: binance does not have market symbol PINGPONG/USDT
2025-10-17T22:10:11.745109671Z [inf]  ❌ XTER/USDT veri çekme hatası: binance does not have market symbol XTER/USDT
2025-10-17T22:10:11.745133300Z [inf]  📊 Tarama tamamlandı. Yeni sinyal yok.
2025-10-17T22:10:11.745147899Z [inf]  ⚠️ 286 sembol hatası (normal)
2025-10-17T22:10:11.745164607Z [inf]  Portfolio state error: {'message': "Could not find the table 'public.portfolio_state' in the schema cache", 'code': 'PGRST205', 'hint': None, 'details': None}
2025-10-17T22:10:11.745178498Z [inf]  💰 Portföy Durumu: $1000.00 (Kullanılabilir: $1000.00)
2025-10-17T22:10:14.113960356Z [inf]  Portfolio state error: {'message': "Could not find the table 'public.portfolio_state' in the schema cache", 'code': 'PGRST205', 'hint': None, 'details': None}
2025-10-17T22:10:14.113968442Z [inf]  INFO:     100.64.0.5:61594 - "GET /api/portfolio HTTP/1.1" 200 OK
2025-10-17T22:10:17.039554647Z [inf]  INFO:     100.64.0.4:28694 - "GET /api/trades/open HTTP/1.1" 200 OK
2025-10-17T22:11:17.579391832Z [inf]  INFO:     100.64.0.7:50844 - "GET /api/signals?limit=50 HTTP/1.1" 200 OK
2025-10-17T22:11:17.579400476Z [inf]  INFO:     100.64.0.7:50852 - "GET /health HTTP/1.1" 200 OK
2025-10-17T22:11:17.579406139Z [inf]  INFO:     100.64.0.7:50862 - "GET /api/trades/open HTTP/1.1" 200 OK
2025-10-17T22:11:17.579412849Z [inf]  INFO:     100.64.0.7:50872 - "GET /api/trades/closed HTTP/1.1" 200 OK
2025-10-17T22:11:17.579935435Z [inf]  INFO:     100.64.0.6:26974 - "OPTIONS /api/signals?limit=50 HTTP/1.1" 200 OK
2025-10-17T22:11:17.579943423Z [inf]  INFO:     100.64.0.6:26990 - "OPTIONS /api/portfolio HTTP/1.1" 200 OK
2025-10-17T22:11:17.579950756Z [inf]  INFO:     100.64.0.6:26994 - "OPTIONS /api/trades/closed HTTP/1.1" 200 OK
2025-10-17T22:11:17.579960502Z [inf]  INFO:     100.64.0.6:27012 - "OPTIONS /api/trades/open HTTP/1.1" 200 OK
2025-10-17T22:11:17.579968742Z [inf]  INFO:     100.64.0.6:27016 - "OPTIONS /health HTTP/1.1" 200 OK
2025-10-17T22:11:17.579976736Z [inf]  INFO:     100.64.0.6:27008 - "OPTIONS /api/markets HTTP/1.1" 200 OK
2025-10-17T22:11:17.579984616Z [inf]  INFO:     100.64.0.6:27038 - "OPTIONS /api/signals/stats HTTP/1.1" 200 OK
2025-10-17T22:11:17.579991837Z [inf]  INFO:     100.64.0.7:50820 - "OPTIONS /api/signals?limit=50 HTTP/1.1" 200 OK
2025-10-17T22:11:17.580001147Z [inf]  INFO:     100.64.0.7:50834 - "OPTIONS /api/trades/open HTTP/1.1" 200 OK
2025-10-17T22:11:17.580008351Z [inf]  INFO:     100.64.0.7:50844 - "OPTIONS /health HTTP/1.1" 200 OK
2025-10-17T22:11:17.580015853Z [inf]  INFO:     100.64.0.7:50852 - "OPTIONS /api/signals/stats HTTP/1.1" 200 OK
2025-10-17T22:11:17.580022730Z [inf]  INFO:     100.64.0.7:50862 - "OPTIONS /api/portfolio HTTP/1.1" 200 OK
2025-10-17T22:11:17.580030681Z [inf]  INFO:     100.64.0.7:50872 - "OPTIONS /api/markets HTTP/1.1" 200 OK
2025-10-17T22:11:17.580037771Z [inf]  INFO:     100.64.0.7:50884 - "OPTIONS /api/trades/closed HTTP/1.1" 200 OK
2025-10-17T22:11:17.580045466Z [inf]  INFO:     100.64.0.7:50884 - "GET /api/markets HTTP/1.1" 200 OK
2025-10-17T22:11:17.580052854Z [inf]  Portfolio state error: {'message': "Could not find the table 'public.portfolio_state' in the schema cache", 'code': 'PGRST205', 'hint': None, 'details': None}
2025-10-17T22:11:17.580061046Z [inf]  INFO:     100.64.0.7:50834 - "GET /api/portfolio HTTP/1.1" 200 OK
2025-10-17T22:11:17.580076892Z [inf]  INFO:     100.64.0.7:50820 - "GET /api/signals/stats HTTP/1.1" 200 OK
2025-10-17T22:11:23.000000000Z [inf]  Stopping Container