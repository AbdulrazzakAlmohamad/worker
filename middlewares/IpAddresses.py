class IpAddresses:
    ipAddresses = [  # here you can add an Ip you want to use our services
        "185.197.196.13",
        "185.197.196.10"
        # "127.0.0.1"
    ]

    def check(self, ip):
        return ip in self.ipAddresses
