using System;
using System.IO;
using System.Net.Sockets;
using System.Text;
using System.Collections;

// c:\Windows\Microsoft.NET\Framework\v4.0.30319\csc.exe /target:library svgzHandler.cs

namespace RobotBerry
{
    public class Connector
    {
        private TcpClient client;
        private NetworkStream stream;

        public Connector() { }
        public Connector(String ip, Int32 port)
        {
            try
            {
                client = new TcpClient(ip, port);
                Console.WriteLine("init TCP connection");
                stream = client.GetStream();
                Console.WriteLine("init Network stream");
            }
            catch (Exception e)
            {
                Console.WriteLine(e.ToString());
            }
        }

        public void Send(string message)
        {
            if (client == null || stream == null || message == String.Empty) return;

            try {
                Byte[] data = System.Text.Encoding.ASCII.GetBytes(message);
                stream.Write(data, 0, data.Length);
                Console.WriteLine("Sent: {0}", message);

                Int32 bytes = stream.Read(data, 0, data.Length);
                String responseData = String.Empty;
                responseData = System.Text.Encoding.ASCII.GetString(data, 0, bytes);
                Console.WriteLine("Received: {0}", responseData);
            }
            catch(Exception e)
            {
                Console.WriteLine(e.ToString());
            }
        }

        ~Connector()
        {
            stream.Close();
            client.Close();
        }
    }
}