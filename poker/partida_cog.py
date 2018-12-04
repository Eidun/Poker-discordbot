from discord.ext import commands
import asyncio
import discord
import poker.models as models
import data
import poker.imagecards as imagecards


class Poker:
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.ronda = False
        self.nuevos = False
        self.jugadores = {}
        self.baraja = None
        self.mensaje_cartas = None
        self.cartas_mesa = []
        self.siguientes = [3, 1, 1]
        self.estado = 0
        self.channel = None

    @commands.command(pass_context=True)
    async def cartas(self, ctx, *pseudonimo):
        """Pide cartas al croupier"""
        if not self.ronda:
            await self.bot.say('No hay una ronda de póker a la que puedas unirte')
            return
        player = ctx.message.author

        if pseudonimo.__len__() == 0:
            pseudonimo = player.display_name
        else:
            pseudonimo = ' '.join(palabra for palabra in pseudonimo)

        if player.id not in self.jugadores:
            self.jugadores[player.id] = [player, {pseudonimo: [self.baraja.sacar_carta(), self.baraja.sacar_carta()]}]
        else:
            if pseudonimo in self.jugadores[player.id][1]:
                await self.bot.say('Ya estás en esta partida!')
                return
            self.jugadores[player.id][1][pseudonimo] = [self.baraja.sacar_carta(), self.baraja.sacar_carta()]

        await self.bot.say(f'Bienvenido a la partida, {pseudonimo}')

        await self.bot.send_file(player,
                                 imagecards.get_image_card(pseudonimo, self.jugadores[player.id][1][pseudonimo]),
                                 content=pseudonimo)

    @commands.command(pass_context=True)
    @commands.has_permissions(administrator=True)
    async def seguir(self, ctx):
        """Saca la siguientes cartas"""
        if not self.ronda:
            await self.bot.say('No hay una ronda de póker disponible')
            return
        if self.mensaje_cartas is not None:
            await self.bot.delete_message(self.mensaje_cartas)
        self.nuevos = False
        siguientes = self.siguientes[self.estado]
        for i in range(siguientes):
            self.cartas_mesa.append(self.baraja.sacar_carta())
        self.estado += 1
        self.mensaje_cartas = await self.bot.send_file(self.channel,
                                                       imagecards.get_image_card('Laguna Gris S.A.', self.cartas_mesa))
        if self.estado == 3:
            self.estado = 0
            await self.bot.send_message(self.channel,
                                        'Todas las cartas sobre la mesa, veamos qué secretos nos aguardan.')

    @commands.command(pass_context=True, name='ronda')
    @commands.has_permissions(administrator=True)
    async def nueva_ronda(self, ctx):
        """Comienza una nueva ronda"""
        server = ctx.message.server
        permissions = discord.PermissionOverwrite(send_messages=False)
        mine = discord.PermissionOverwrite(send_messages=True)
        self.channel = await self.bot.create_channel(ctx.message.server, 'mesa', (server.default_role, permissions),
                                                     (server.me, mine))
        await self.bot.send_message(self.channel, 'No escribais en la mesa, es para poder ver las cartas fácilmente')
        self.ronda = True
        self.nuevos = True
        self.baraja = models.Baraja()
        await self.bot.say(
            'Nueva ronda de póker. Jugadores, utilizad ``!cartas`` para participar una vez tengais la apuesta mínima.')

    @commands.command(pass_context=True, name='terminar')
    @commands.has_permissions(administrator=True)
    async def fin_ronda(self, ctx: commands.Context):
        """Termina la ronda actual."""
        self.ronda = False
        self.nuevos = False
        self.jugadores.clear()
        self.cartas_mesa.clear()

        await self.bot.say('Ronda finalizada. Cerrando la mesa...')
        await asyncio.sleep(5)
        self.mensaje_cartas = None
        await self.bot.delete_channel(self.channel)

    @commands.command(pass_context=True)
    async def participantes(self, ctx):
        """Muestra los personajes que usas"""
        player = ctx.message.author
        if player.id not in self.jugadores:
            await self.bot.say('No estás jugando con nadie')
            return
        message = 'Jugadores:\n'
        message += '\n'.join(jugador for jugador in self.jugadores[player.id][1])
        await self.bot.say(message)

    @commands.command(pass_context=True)
    async def revelar(self, ctx, modo='Flojo'):
        """revelar Enseña tu mano. <!revelar tensión> para añadir suspense!!"""
        player = ctx.message.author
        if player.id not in self.jugadores:
            await self.bot.say('No estás participando. ¿Qué quieres revelar?')
            return
        if modo == 'tension':
            await self.bot.send_message(ctx.message.channel, '...')
            await self.bot.send_typing(ctx.message.channel)
            await asyncio.sleep(8)
        for name, cards in self.jugadores[player.id][1].items():
            await self.bot.send_file(ctx.message.channel, imagecards.get_image_card(name, self.cartas_mesa),
                                     content='Mesa')
            await self.bot.send_file(ctx.message.channel, imagecards.get_image_card(name, cards), content=name)

    @commands.command(pass_context=True)
    async def revelar_pj(self, ctx, *pseudonimo):
        player = ctx.message.author
        if player.id not in self.jugadores:
            await self.bot.say('No estás participando. ¿Qué quieres revelar?')
            return

        pseudonimo = ' '.join(palabra for palabra in pseudonimo)

        if pseudonimo not in self.jugadores[player.id][1]:
            await self.bot.say('Ese nombre no está en la partida')
            return

        cards = self.jugadores[player.id][1][pseudonimo]

        await self.bot.send_file(ctx.message.channel, imagecards.get_image_card(pseudonimo, self.cartas_mesa),
                                 content='Mesa')
        await self.bot.send_file(ctx.message.channel, imagecards.get_image_card(pseudonimo, cards), content=pseudonimo)


def setup(bot: commands.Bot):
    bot.add_cog(Poker(bot))
