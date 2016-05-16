# Maintainer: Michal Krenek (Mikos) <m.krenek@gmail.com>
pkgname=mensahangupsbot
pkgver=0.2.3
pkgrel=1
pkgdesc="MensaBot for Google Hangouts"
arch=('any')
url="https://github.com/TimRepke/hangupsbot"
license=('GPL3')
depends=('hangups-git' 'python-appdirs', 'beautifulsoup4')
makedepends=('python-setuptools')
source=(https://github.com/TimRepke/hangupsbot/archive/v$pkgver.tar.gz)

build() {
  cd "$srcdir/$pkgname-$pkgver"
  python setup.py build
}

package() {
  cd "$srcdir/$pkgname-$pkgver"
  python setup.py install --root="$pkgdir"
}

# vim:set ts=2 sw=2 et:
