import discord
import random
import pymysql
import time
import datetime
import threading
from discord.ext import commands

# 自定義例外
class CompensateError(Exception):
    def __str__(self):
        return '請給非補償刀的人來下指令哦'

class NotYouError(Exception):
    def __str__(self):
        return '你沒有報名這個王哦!!'

class CantSignUpError(Exception):
    def __str__(self):
        content = '現在是第 {} 周哦!! 所以只能報 {} 跟 {} 周哦!! 醒醒!!☆'.format(current_week,current_week,current_week+1)
        return content

class YouDontExistError(Exception):
    def __str__(self):
        return '咦?怎麼找不到你呢??'

class GGIndexError(Exception):
    def __str__(self):
        return '咦?現在不是 %s 王嗎?'%(current_boss_num)


# parameters
account = ''
passwords = ''

gbl_post_channel = 698583084982861844
lobby_channel = 673197179099414552

client = commands.Bot(command_prefix = '.')
client.remove_command('help')

# 事件觸發
@client.event
async def on_ready():
    # 更改狀態
    #'.pekohelp 等著被餵食的佩可(´・ω・`)'
    await client.change_presence(activity=discord.Game('凱留 .pekohelp'))
    print('on line')


@client.event
async def on_member_join(member):
    # 聊天室ID : 673197179099414552
    # 公告訊息ID : 673356657061003304
    # 使用者ID : member.id
    # 查詢區ID : 673376127846318111
    
    text_master = client.get_user(643868597642592277) # 會長物件
    text_submaster1 = client.get_user(150839354648952832) # 副會長物件
    text_submaster2 = client.get_user(413480240627712010) # 副會長物件
    text_member = client.get_user(member.id) # 進入人員訊息物件
    text_channel = client.get_channel(673356657061003304)  # 公告訊息物件
    content_part1 = '阿囉哈!!~☆ %s ちゃん 歡迎你加入雪月星塵\n\
我是可愛的貪吃佩可~☆\n\
%s 醬，麻煩請先到 %s 頻道中閱讀公告，同意後請點選表情領取會員身分(如下圖)\n'%(text_member.mention,text_member.mention,text_channel.mention)
    content_part2 = '點選成員名單中的自己確認領取會員身分後才能進行報刀等操作哦!!~\n(如何確認請參考下圖)\n'
    content_part3 = '完成以上步驟算是完成加入哦!!否則會被 %s %s %s 盯上的( Φ ω Φ )。\n\
讓我們一起吃遍戰隊戰的王吧!!~  やばいですね!!~☆'%(text_master.mention,text_submaster1.mention,text_submaster2.mention)
    
    for i,uid in enumerate([member.id,lobby_channel]):
        if i == 0:
            channel = client.get_user(uid)
        else:
            channel = client.get_channel(uid)

        apx1 = discord.File('image/apx1.png')
        apx2 = discord.File('image/apx2.png')
        await channel.send(content_part1)
        await channel.send(file=apx1)
        await channel.send(content_part2)
        await channel.send(file=apx2)
        await channel.send(content_part3)
        apx1.close()
        apx2.close()
  

# 指令觸發
@client.command()
async def pekohelp(ctx):
    embed = discord.Embed(title="P醬的AI佩可", description="我是可愛的貪吃佩可", color=0xffff00)
    embed.add_field(name="官網連結", value=".os", inline=True)
    embed.add_field(name="日版twitter連結", value=".jptwitter", inline=True)
    embed.add_field(name="蘭德索爾圖書館", value=".wiki", inline=True)
    embed.add_field(name="戰隊戰報名", value=".su <第幾週> <王順序> <補償刀y,n> <備註>\nex. 報名第4週3王，不是補償刀\n.su 4 3 n", inline=True)
    embed.add_field(name="戰隊戰取消", value=".cc <第幾週> <王順序>\nex. 取消第4週3王\n.cc 4 3", inline=True)
    embed.add_field(name="戰隊戰報名名單\n若不設定周目則為當前周目", value=".gbl\n.gbl <指定周目>", inline=True)
    embed.add_field(name="設定當前週目", value=".cwk <當前週目> <當前王順序>", inline=True)
    embed.add_field(name="今日人員出刀數", value=".today", inline=True)
    embed.add_field(name="提醒", value=".note <王順序>", inline=True)
    embed.add_field(name="check in", value=".ci ", inline=True)
    embed.add_field(name="擊殺王通知，並提醒下個王的人員", value=".gg <王順序>", inline=True)
    embed.add_field(name="閃退紀錄", value=".gg 或.閃退", inline=True)
    await ctx.send(embed=embed)

@client.command(aliases=['peko','aipeko','pekorinu'])
async def _peko(ctx):
    content = ['阿囉哈!!~☆',
    '你要給我食物嗎? 我可以喜歡上你嗎?(ﾉ>ω<)ﾉ',
    '嗨嗨!!~']
    await ctx.send(random.choice(content))

@client.command()
async def os(ctx):
    content = '阿囉哈!!~☆  這是官方網站哦~\nhttp://www.princessconnect.so-net.tw/news'
    await ctx.send(content)

@client.command()
async def jptwitter(ctx):
    content = '阿囉哈!!~☆  這是日版官方twitter哦~\nhttps://mobile.twitter.com/priconne_redive'
    await ctx.send(content)

@client.command()
async def wiki(ctx):
    content = '阿囉哈!!~☆  這是蘭德索爾圖書館哦~\nhttps://pcredivewiki.tw/'
    await ctx.send(content)

@client.command()
async def dejavu(ctx):
    content = 'https://nhentai.net/random/'
    await ctx.send(content)


################## 戰隊戰相關指令 ####################

# 設定當前周目
@client.command()
async def cwk(ctx,week,num=1):
    if week.isdigit() and int(week) > 0:
        global current_week
        global current_boss_num
        current_week = int(week)
        current_boss_num = int(num)
        await ctx.send("好哦 %s ちゃん!! 現在吃王之旅已經到了 %s 週 %s 王啦!! 亞拜伊爹斯捏!!~☆"%(ctx.author.display_name,current_week,current_boss_num))
    else:
        await ctx.send(" %s ちゃん!! 不要亂啦!!(／‵Д′)／~ ╧╧"%(ctx.author.display_name))

# 報名出刀
@client.command()
async def su(ctx, step=None, index=None, compensate='n', notation=''):
    try:
        if int(step) <= 0:
            raise NameError
        elif int(step) < current_week or int(step) > current_week+1:
            raise CantSignUpError
        elif int(index) > 5 and int(index) < 1:
            await ctx.send('%s ちゃん，只有5隻王啦!!'%(ctx.author.display_name))
        else:
            # 呼叫訊息使用者名稱 : ctx.author.display_name
            # 呼叫訊息使用者id : ctx.author.id
            # 呼叫訊息時間 : ctx.message.created_at
            create_time = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
            
            compensate_dic = {'y':1, 'n':0}
            conn = pymysql.connect(host='192.168.0.102',port=3307,db='PCRedive',user=account,password=passwords)
            cur = conn.cursor()

            if int(step) == current_week and int(index) == current_boss_num:
                check_in = '1'
            else:
                check_in = '0'

            cur.execute("insert into GuildBattleList(member_id,create_time,step,GuildBattleList.index,compensate,check_in,notation) \
values (%s,%s,%s,%s,%s,%s,%s)",(ctx.author.id,create_time,step,index,compensate_dic[compensate.lower()],check_in,notation))
            conn.commit()
            cur.close()
            conn.close()
            await ctx.send('%s ちゃん，報名完成囉!!'%(ctx.author.display_name))
            # 傳送至出刀查詢區
            query_channel = client.get_channel(gbl_post_channel)
            await query_channel.purge()
            await gbl(ctx,str(int(current_week)))
            await gbl(ctx,str(int(current_week)+1))
    except NameError:
        await ctx.send('唔...佩可剛睡醒!! 可以跟我說現在第幾週嗎?~☆(請用 ".cwk" 告訴我哦!!)')
    except CantSignUpError as csue:
        await ctx.send(csue)
    except Exception as e:
        print(e)
        await ctx.send('%s ちゃん，指令好像有打錯哦~  請再檢查一下!!☆'%(ctx.author.display_name))
    
# 取消報名
@client.command()
async def cc(ctx, *arg):
    try:
        post_channel = client.get_channel(gbl_post_channel)
        
        step = arg[0]
        index = arg[1]
        compensate = arg[2]
        compensate_dic = {'y':1, 'n':0}
        conn = pymysql.connect(host='192.168.0.102',port=3307,db='PCRedive',user=account,password=passwords)
        cur = conn.cursor()
        cur.execute("select * from GuildBattleList where GuildBattleList.member_id=%s and step=%s and GuildBattleList.index=%s and compensate=%s",(ctx.author.id,step,index,compensate_dic[compensate.lower()]))

        if len(cur.fetchall()) != 0:
            cur.execute("delete from GuildBattleList where GuildBattleList.member_id=%s and step=%s and GuildBattleList.index=%s and compensate=%s",(ctx.author.id,step,index,compensate_dic[compensate.lower()]))
            cur.execute("insert into DeleteRecord(member_id,create_time,step,DeleteRecord.index,compensate) values (%s,%s,%s,%s,%s)",(ctx.author.id,ctx.message.created_at,int(step),int(index),compensate_dic[compensate.lower()]))
            conn.commit()
            await ctx.send('%s ちゃん，已經成功取消囉!!'%(ctx.author.display_name))
        else:
            raise YouDontExistError
        
        # 傳送至出刀查詢區
        query_channel = client.get_channel(gbl_post_channel)
        await query_channel.purge()
        await gbl(ctx,str(int(current_week)))
        await gbl(ctx,str(int(current_week)+1))
    except YouDontExistError as ydee:
        await ctx.send(ydee)
    except Exception as e:
        print(e)
        await ctx.send('%s ちゃん，指令好像有打錯哦~  請再檢查一下!!☆'%(ctx.author.display_name))
    finally:
        cur.close()
        conn.close()


# 當前周目報名清單
@client.command()
async def gbl(ctx,*arg):
    try:
        if len(arg) == 0:
            week = current_week
        else:
            week = int(arg[0])

        conn = pymysql.connect(host='192.168.0.102',port=3307,db='PCRedive',user=account,password=passwords)
        cur = conn.cursor()
        cur.execute("select m.member_name, g.index, g.compensate , g.notation, g.check_in \
from GuildBattleList as g join members as m \
on g.member_id = m.member_id where g.step = %s order by compensate desc, create_time;",(week))
        
        name_list = [[],[],[],[],[]]
        member_string_dic = {}
        checkin_dic = {0:'未回應', 1:'已回應'}
        for name,index,c,notation,checkin in cur.fetchall():
            if c == 1:
                name_list[index-1].append(checkin_dic[checkin]+' - (補償) '+name+' '+notation)
            else:
                name_list[index-1].append(checkin_dic[checkin]+' - '+name+' '+notation)
        
        for i,e in enumerate(name_list):
            if len(e) != 0:
                member_string_dic[i] = '\n'.join(e)
            else:
                member_string_dic[i] = '目前無人報名呦~(ﾉ>ω<)ﾉ'

        embed=discord.Embed(title="%s周目戰隊戰報名名單"%(week), color=0xffff00)
        embed.add_field(name="【一王】", value=member_string_dic[0], inline=False)
        embed.add_field(name="【二王】", value=member_string_dic[1], inline=False)
        embed.add_field(name="【三王】", value=member_string_dic[2], inline=False)
        embed.add_field(name="【四王】", value=member_string_dic[3], inline=False)
        embed.add_field(name="【五王】", value=member_string_dic[4], inline=False)

        query_channel = client.get_channel(gbl_post_channel)
        await query_channel.send(embed=embed)
        #await ctx.send(embed=embed)
    except NameError:
        await ctx.send('唔...佩可剛睡醒!! 可以跟我說現在第幾週嗎?~☆(請用 ".cwk" 告訴我哦!!)')
    except Exception as e:
        print(e)
        await ctx.send('%s ちゃん，指令好像有打錯哦~  請再檢查一下!!☆'%(ctx.author.display_name))
    finally:
        cur.close()
        conn.close()

# 建立人員清單
@client.command()
async def mlist(ctx):
    # ctx.guild.members 回傳使用指令伺服器的人員清單 list
    # member.roles 獲取人員身分組
    check_roles = set(['會員','會長','副會長'])
    member_list = ctx.guild.members
    conn = pymysql.connect(host='192.168.0.102',port=3307,db='PCRedive',user=account,password=passwords)
    cur = conn.cursor()

    cur.execute("select * from members")
    current_members_id = [m[1] for m in cur.fetchall()]  # 將id儲存成list

    for member in member_list:
        if member.nick is None:
            insert_name = member.name
        else:
            insert_name = member.nick
        
        member_roles = set([role.name for role in member.roles])
        if (len(member_roles & check_roles) == 0) and (member.id in current_members_id):
            # 如果當前身分組集合內沒有指定身分組且id在現有名單內，則進行刪除
            cur.execute("delete from members where member_id=%s",(member.id))
        elif (len(member_roles & check_roles) != 0) and (member.id not in current_members_id):
            # 如果當前身分組集合內有指定身分組且id沒有現有名單內，則進行新增
            cur.execute("insert into members(member_name,member_id) values (%s,%s)",(insert_name,member.id))

    conn.commit()
    cur.close()
    conn.close()

# 查詢今天出刀狀況
@client.command()
async def today(ctx):
    if int(datetime.datetime.now().strftime('%H')) < 5:
        start = datetime.date.today() - datetime.timedelta(days=1)
        end = datetime.date.today()
    else:
        start = datetime.date.today()
        end = datetime.date.today() + datetime.timedelta(days=1)

    conn = pymysql.connect(host='192.168.0.102',port=3307,db='PCRedive',user=account,password=passwords)
    cur = conn.cursor()
    cur.execute("select m.member_name, count(g.member_id) \
from members as m left outer join \
(select * from GuildBattleList as sg \
where sg.compensate = 0 and \
sg.create_time between '%s 05:00:00' and '%s 05:00:00')g \
on m.member_id = g.member_id \
group by m.member_id order by count(g.member_id)" % (start.strftime('%Y-%m-%d'), end.strftime('%Y-%m-%d')))

    content = ''
    for info in cur.fetchall():
        content += '%-15s : %s / 3\n'% info
    embed=discord.Embed(title="%s 會員登記出刀數"%(start.strftime('%Y-%m-%d')), description=content, color=0xffff00)
    cur.close()
    conn.close()
    await ctx.send(embed=embed)

# 通知
@client.command()
async def note(ctx,index):
    try:
        conn = pymysql.connect(host='192.168.0.102',port=3307,db='PCRedive',user=account,password=passwords)
        cur = conn.cursor()

        cur.execute("select distinct member_id from GuildBattleList \
    where step=%s and GuildBattleList.index=%s",(current_week,index))

        mention_list = [client.get_user(e[0]).mention for e in cur.fetchall()]
        cur.close()
        conn.close()

        if len(mention_list) != 0:
            memtion_content = '\t'.join(mention_list) + '\n準備上場囉!! がんばれ~がんばれ~!!☆'
        else:
            memtion_content = '咦?  怎麼沒有人呢? (失望'
        await ctx.send(memtion_content)
    except:
        await ctx.send('唔...佩可剛睡醒!! 可以跟我說現在第幾週嗎?~☆(請用 ".cwk" 告訴我哦!!)')


# 等待
def waitmember(ctx,current_week,current_boss_num):
    time.sleep(600)

    conn = pymysql.connect(host='192.168.0.102',port=3307,db='PCRedive',user=account,password=passwords)
    cur = conn.cursor()
    cur.execute("delete from GuildBattleList where \
GuildBattleList.step=%s and GuildBattleList.index=%s and check_in=0",(current_week,current_boss_num))
    conn.commit()
    cur.close()
    conn.close()

    #asyncio.run(gbl(ctx,str(int(current_week))))
    #asyncio.run(gbl(ctx,str(int(current_week)+1)))


# 擊殺王後通知及處理
@client.command()
async def gg(ctx,index,member_id=None):
    try:
        if member_id == None: member_id = ctx.author.id
        if int(index) < 1 or int(index) > 5: raise Exception
        if int(index) != current_boss_num: raise GGIndexError

        create_time = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
        conn = pymysql.connect(host='192.168.0.102',port=3307,db='PCRedive',user=account,password=passwords)
        cur = conn.cursor()
        cur.execute("insert into GGRecord(from_member_id,to_member_id,GGRecord.step,GGRecord.index,create_time) \
values (%s,%s,%s,%s,%s)",(ctx.author.id,member_id,current_week,index,create_time))
        conn.commit()
        
        if int(index) != 5:
            await cwk(ctx,str(current_week),num=int(index)+1)
        else:
            await cwk(ctx,str(int(current_week)+1))
        
        await note(ctx,current_boss_num)
        cur.close()
        conn.close()

        # 執行計時，時間到沒回應就刪除
        #print(current_week,current_boss_num)
        
        waitjob = threading.Thread(target=waitmember,args=(ctx,current_week,current_boss_num,))
        waitjob.start()
        
    except NameError:
        await ctx.send('唔...佩可剛睡醒!! 可以跟我說現在第幾週嗎?~☆(請用 ".cwk" 告訴我哦!!)')
    except NotYouError as nye:
        await ctx.send(nye)
    except GGIndexError as ggie:
        await ctx.send(ggie)
    except CompensateError as ce:
        await ctx.send(ce)
    except Exception as e:
        print(e)
        await ctx.send('%s ちゃん，指令好像有打錯哦~  請再檢查一下!!☆'%(ctx.author.display_name))

# 出刀前確認
@client.command(aliases=['checkin','ci'])
async def _checkin(ctx):
    try:
        conn = pymysql.connect(host='192.168.0.102',port=3307,db='PCRedive',user=account,password=passwords)
        cur = conn.cursor()

        cur.execute("select distinct member_id from GuildBattleList as g where \
g.step=%s and g.index=%s",(current_week,current_boss_num))
        su_id = [int(e[0]) for e in cur.fetchall()]
        if int(ctx.author.id) not in su_id: raise NotYouError

        cur.execute("update GuildBattleList as g set check_in=1 where \
g.member_id=%s and g.step=%s and g.index=%s",(ctx.author.id,current_week,current_boss_num))
        conn.commit()
        cur.close()
        conn.close()
        query_channel = client.get_channel(gbl_post_channel)
        await ctx.send("啊!! %s ちゃん 你來啦!! 加油加油!!(ﾉ>ω<)ﾉ"%(ctx.author.display_name))
        await query_channel.purge()
        await gbl(ctx,str(int(current_week)))
        await gbl(ctx,str(int(current_week)+1))
    except NotYouError as nye:
        await ctx.send("現在進度是 %s 週目 %s 王"%(current_week,current_boss_num))
        await ctx.send(nye)
    except Exception as e:
        print(e)
        await ctx.send('%s ちゃん，指令好像有打錯哦~  請再檢查一下!!☆'%(ctx.author.display_name))

# 閃退註記
@client.command(aliases=['qq','閃退'])
async def _qq(ctx):
    if int(datetime.datetime.now().strftime('%H')) < 5:
        start = datetime.date.today() - datetime.timedelta(days=1)
        end = datetime.date.today()
    else:
        start = datetime.date.today()
        end = datetime.date.today() + datetime.timedelta(days=1)

    create_time = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
    conn = pymysql.connect(host='192.168.0.102',port=3307,db='PCRedive',user=account,password=passwords)
    cur = conn.cursor()
    cur.execute("select * from SLRecord where member_id=%s and create_time between \
'%s 05:00:00' and '%s 05:00:00'"%(ctx.author.id,start.strftime('%Y-%m-%d'),end.strftime('%Y-%m-%d')))

    if len(cur.fetchall()) == 0:
        cur.execute("insert into SLRecord values (%s,%s)",(ctx.author.id,create_time))
        conn.commit()
        await ctx.send("嗚~  %s ちゃん 不要氣餒!! 閃退後繼續加油!! d(`･∀･)b"%(ctx.author.display_name))
    else:
        await ctx.send("嗚~  %s ちゃん 今天你閃退過囉!! 先乖乖地在樹上等一下哦~☆"%(ctx.author.display_name))
    
    cur.close()
    conn.close()
    

client.run("")