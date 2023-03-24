import android_auto_play_opencv as am
from random import randint as ran

adbpath = 'C:/Users/seiki/anaconda3/envs/python_vscode/'

def ijhantei(x,y):
    #行について-------------
    if 1250 <= y <= 1350:
        gyou=6
    elif 1150<=y <= 1250:
        gyou=5
    elif 1000<=y <= 1150:
        gyou=4
    elif 900<=y <= 1000:
        gyou=3
    elif 800 <=y <= 900:
        gyou=2
    elif 680 <=y <= 800:
        gyou=1
    elif 550 <=y <= 680:
        gyou=0
    elif 200 <=y <= 500:
        gyou='master'

    #列について--------------
    if 50 <= x <= 150:
        retu=0
    elif 150<=x<= 280:
        retu=1
    elif 280<=x<= 400:
        retu=2
    elif 400<=x<= 550:
        retu=3
    elif 550<=x<= 670:
        retu=4
    
    return gyou,retu

def j_to_x(j):
    if j ==0:
        xzahyou=93
    elif j==1:
        xzahyou=226
    elif j==2:
        xzahyou=359
    elif j==3:
        xzahyou=492
    elif j==4:
        xzahyou=625
    return xzahyou

def main():

    aapo = am.AapoManager(adbpath)
    
    while True:
        # 画面キャプチャ
        aapo.screencap()

        #広告対策--------------------------
        if aapo.touchImg('target_2048\\datas\\ads\\ad1.png'):
            aapo.sleep(1)
        
        if aapo.touchImg('target_2048\\datas\\ads\\ad2.png'):
            aapo.sleep(1)
        
        if aapo.touchImg('target_2048\\datas\\ads\\ad3.png'):
            aapo.sleep(1)

        if aapo.touchImg('target_2048\\datas\\ads\\ad4.png'):
            aapo.sleep(1)

        if aapo.touchImg('target_2048\\datas\\ads\\ad5.png'):
            aapo.sleep(1)

        if aapo.touchImg('target_2048\\datas\\ads\\ad6.png'):
            aapo.sleep(1)

        if aapo.touchImg('target_2048\\datas\\ads\\ad7.png'):
            aapo.sleep(1)
        
        if aapo.touchImg('target_2048\\datas\\ads\\ad8.png'):
            aapo.sleep(1)
        
        
        #ゲーム画面制御---------------------
            #タイトル画面のスタートボタン
        if aapo.touchImg('target_2048\\datas\\gameplay\\PLAY.png'):     
            aapo.sleep(3)

            #ポップアップの閉じるボタン
        if aapo.touchImg('target_2048\\datas\\gameplay\\toziru.png'):
            aapo.sleep(3)

            #ゲームスタートボタン
        if aapo.touchImg('target_2048\\datas\\gameplay\\gamestart.png'):
            aapo.sleep(10)
        
            #playstoreに飛んだ時
        if aapo.chkImg('target_2048\\datas\\gameplay\\playstore.png'):
            aapo.inputkeyevent(3)
            aapo.sleep(3)
            if aapo.touchImg('target_2048\\datas\\gameplay\\gamestart2.png'):
                aapo.sleep(5)

            #webサイトに飛んだ時
        if aapo.chkImg('target_2048\\datas\\gameplay\\web.png'):
            aapo.inputkeyevent(3)
            if aapo.touchImg('target_2048\\datas\\gameplay\\gamestart2.png'):
                aapo.sleep(5)
        
        #ゲームプレイ--------------------
        if aapo.chkImg('target_2048\\datas\\gameplay\\kakunin.png'):
                #画面情報の保存
            pazuru=[[0,0,0,0,0],
                    [0,0,0,0,0],
                    [0,0,0,0,0],
                    [0,0,0,0,0],
                    [0,0,0,0,0],
                    [0,0,0,0,0],
                    [0,0,0,0,0]]
            #変数
            xzahyou=0
            gyou=0
            retu=0
                #数字の読み取り--------------
            nums=(16,32,64,128,256,512,1024)
            for num in nums :
                ret, poss = aapo.chkImg2(f'target_2048\\datas\\nums\\num{num}.png',_multi = True)
                if ret:
                    for i in range(len(poss)):

                        pos = poss[i]
                        x,y=pos[0],pos[1]
                        gyou,retu=ijhantei(x,y)
                        if gyou == 'master':
                            master = num
                            continue
                        else:
                            pazuru[gyou][retu]=num
                        pass
                    pass
            #現在の数字があるか見つける
            masterlist_i=[]
            masterlist_j=[]
            for i in range(7):
                i=6-i
                for j in range(5):
                    if pazuru[i][j] == master:
                        masterlist_i.append(i)
                        masterlist_j.append(j)
                
            #数字を落としていく------------------
            if len(masterlist_j) != 0: #数字の上に落とせるとき
                for i in range(len(masterlist_i)):
                    if pazuru[masterlist_i[i]-1][masterlist_j[i]]==0:
                        xzahyou=j_to_x(masterlist_j[i])
                        aapo.longTouchPos(xzahyou+ran(-20,20), 800+ran(-200,200), 500+ran(-250,100))
                        break
                    elif masterlist_i[i] == 0:
                        xzahyou=j_to_x(masterlist_j[i])
                        aapo.longTouchPos(xzahyou+ran(-20,20), 800+ran(-200,200), 500+ran(-250,100))
                        break

            if xzahyou ==0: #上に落とせないとき、数字がなかった時、空白の場所に落とす
                for i in range(7):
                    i=6-i
                    if xzahyou !=0:
                        break
                    else:
                        for j in range(5):
                            if pazuru[i][j] ==0:
                                xzahyou=j_to_x(j)
                                aapo.longTouchPos(xzahyou+ran(-10,20), 800+ran(-200,200), 200+ran(-250,100))
                                break

            else:
                j==1
                xzahyou=j_to_x(j)
                aapo.longTouchPos(xzahyou+ran(-10,20), 800+ran(-200,200), 200+ran(-250,100))

            aapo.sleep(3)

            

if __name__ == '__main__':
    main()