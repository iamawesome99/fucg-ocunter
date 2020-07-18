import discord
import re
import tabulate
from requests import post


class SimpleClient(discord.Client):


        async def count(self, text):


            out_ch = self.get_channel(675162439444332584)
            # out_ch = self.get_channel(635170099925614624)


            # await out_ch.send("still testing, not accurate results")


            m = await out_ch.send("counting (will take a couple minutes)")


            g = self.get_guild(596506186325426219)
            # g = self.get_guild(663627237131812865)




            count = 0
            total = 0
            a = {}


            i = 0


            async with out_ch.typing():


                for ch in g.channels:


                    print("counting (will take a couple minutes)\n#" + ch.name, i, "/", len(g.channels))
                    await m.edit(content="counting (will take a couple minutes)\n#" + ch.name + " " + str(i) + "/" +
                                 str(len(g.channels)))
                    
                    i += 1


                    try:


                        async for msg in ch.history(limit=None):


                            if re.match(".*" + text + ".*", msg.content, flags=re.IGNORECASE):


                                count += 1
                                try:
                                    a[msg.author.name][0] += 1
                                except KeyError:
                                    a[msg.author.name] = [1, 1]
                                    print("new m", msg.author.name)




                            # print(msg.content)
                            total += 1


                            try:
                                a[msg.author.name][1] += 1
                            except KeyError:
                                a[msg.author.name] = [0, 1]
                                print("new m", msg.author.name)
                    


                    except AttributeError:
                        pass

            print("done", count, total)


            await m.delete()


            data = [[str(i), str(j[0]), str(j[1]), str(round(j[0]/j[1] * 100, 2)), str(round(j[0]/count * 100, 2))]
                    for i, j in a.items()]


            data.append(["Total", str(count), str(total), str(round(count/total * 100, 2)), "N/A"])


            table = tabulate.tabulate(data, headers=["Name", "# of " + text, "# of messages", "% of messages with "+text+" in it",
                                                       "contribution % of total "+text], tablefmt='github')
            print(len(table))
            print(table)


            p = post('https://hastebin.com/documents', data=table.encode('utf-8'))
            lnink =  'https://hastebin.com' + '/' + p.json()['key']


            await out_ch.send("Results:\n" + lnink)
                                       


        async def on_message(self, msg):

            com = msg.content.split(" ")

            if com[0] == "f!check" or com[0] == "f!count":
                try:
                    if " ".join(com[1:]) == "":
                        raise KeyError
                    await self.count(" ".join(com[1:]))
                except KeyError:
                    await self.count("fuck")
            if com[0]== "f!help":
                await self.get_channel(675162439444332584).send("f!check or f!count to run\nput text after if you want")

        async def on_ready(self):
            print("bruh")
            # await self.count()
            # exit("21")




a = SimpleClient()


a.run('Njc1MTU5ODQ2ODc3OTIxMjgx.XjzVkg.hN8QQb4BmZL76wGxsVIsxypCgAY')
