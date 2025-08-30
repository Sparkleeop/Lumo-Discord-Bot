import discord
from discord.ext import commands
import socket
import struct
import json
import io
import time

def write_varint(number: int) -> bytes:
    out = b""
    while True:
        temp = number & 0x7F
        number >>= 7
        if number != 0:
            temp |= 0x80
        out += bytes([temp])
        if number == 0:
            break
    return out

def write_string(s: str) -> bytes:
    encoded = s.encode("utf-8")
    return write_varint(len(encoded)) + encoded

def read_varint_from_socket(sock) -> int:
    number = 0
    bytes_read = 0
    while True:
        byte = sock.recv(1)
        if not byte:
            break
        b = byte[0]
        number |= (b & 0x7F) << (7 * bytes_read)
        bytes_read += 1
        if not (b & 0x80):
            break
    return number

def read_varint_from_stream(stream: io.BytesIO) -> int:
    number = 0
    bytes_read = 0
    while True:
        byte = stream.read(1)
        if not byte:
            break
        b = byte[0]
        number |= (b & 0x7F) << (7 * bytes_read)
        bytes_read += 1
        if not (b & 0x80):
            break
    return number

class Minecraft(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.server_ip = "play.wildblocks.fun"
        self.server_port = 19132
        self.protocol_version = 47  # Legacy protocol version; adjust if needed

    @discord.app_commands.command(name="status", description="Check the status and info of WildBlocks MC")
    async def status(self, interaction: discord.Interaction):
        try:
            # Try to establish a connection (timeout after 5 seconds)
            sock = socket.create_connection((self.server_ip, self.server_port), timeout=5)
        except Exception:
            embed = discord.Embed(
                title=":offline: Server Offline",
                description="Could not connect to the server.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed)
            return

        with sock:
            try:
                # Start timer to measure latency
                start_time = time.monotonic()

                # Build handshake packet:
                # Packet ID (0x00) + Protocol Version + Server Address + Server Port + Next State (1 for status)
                packet_id = write_varint(0x00)
                proto = write_varint(self.protocol_version)
                address = write_string(self.server_ip)
                port = struct.pack('>H', self.server_port)
                next_state = write_varint(1)  # 1 for status
                handshake_data = packet_id + proto + address + port + next_state
                handshake_packet = write_varint(len(handshake_data)) + handshake_data

                sock.sendall(handshake_packet)

                # Send status request packet (packet ID 0x00 with no additional data)
                status_request = write_varint(1) + write_varint(0x00)
                sock.sendall(status_request)

                # Read the length of the response (as a VarInt)
                response_length = read_varint_from_socket(sock)
                response_data = b""
                while len(response_data) < response_length:
                    response_data += sock.recv(response_length - len(response_data))

                # Measure latency (in milliseconds)
                latency = int((time.monotonic() - start_time) * 1000)

                # Parse the response:
                buf = io.BytesIO(response_data)
                _ = read_varint_from_stream(buf)  # Packet ID (ignored)
                json_length = read_varint_from_stream(buf)
                json_data = buf.read(json_length).decode("utf-8")
                response_json = json.loads(json_data)

                online = response_json.get("players", {}).get("online", 0)
                max_players = response_json.get("players", {}).get("max", 0)
                version = response_json.get("version", {}).get("name", "Unknown")

                # Replace these emoji IDs with your own custom emoji IDs
                emoji_online = "<:arrow_up:1335164739441004565>"
                emoji_players = "<:Contact:1335165340199686184>"
                emoji_version = "<:earth_cube:1335169800766226473>"
                emoji_latency = "<:high_ping:1335169801886371851>"

                embed = discord.Embed(title="WildBlocks MC Server Status", color=discord.Color.green())
                embed.add_field(name="Status", value=f"{emoji_online} Online", inline=False)
                embed.add_field(name="Players", value=f"{emoji_players} {online}/{max_players}", inline=False)
                embed.add_field(name="Version", value=f"{emoji_version} {version}", inline=False)
                embed.add_field(name="Latency", value=f"{emoji_latency} {latency}ms", inline=False)

                await interaction.response.send_message(embed=embed)
            except Exception as e:
                embed = discord.Embed(
                    title="🚫 Error",
                    description="An error occurred while fetching server status.",
                    color=discord.Color.red()
                )
                await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(Minecraft(bot))
