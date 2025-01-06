class IpAddresses:
    ipAddresses = [  # here you can add an Ip you want to use our services
        "10.10.223.1",
        "10.10.223.2"
        # "127.0.0.1"
    ]

    def check(self, ip):
        return ip in self.ipAddresses
