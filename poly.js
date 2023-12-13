class Poly {
    //https://editor.p5js.org/amygoodchild/sketches/L7X-WH6X0
    constructor(shape, x = 0, y = 0, s = 1, r = 0, closed = true, c = undefined, sc = undefined) {
        // let settings = defaults({
        //     shape: [],
        //     x: 0,
        //     y: 0,
        //     s: 1,
        //     r: 0,
        //     breaks: [],
        // }, arguments)
        this.shape = shape.map((v) => {
            let rv = p5.Vector.rotate(v, r)
            return vec(
                x + rv.x * s,
                y + rv.y * s
            )
        })
        this.closed = closed

        this.inactive = []
        this.inactive.length = this.shape.length
        this.findBBox()

        this.tex = null
        this.c = c
        this.sc = sc

        this.tx = 0
        this.ty = 0
        this.tr = 0

        this.x = 0
        this.y = 0
        this.r = 0
    }

    reloop(idx = undefined) {
        idx = idx ?? floor(rnd(this.shape.length))
        let newshape = []
        for (let i = idx; i < this.shape.length; i++) {
            newshape.push(this.shape[i])
        }
        for (let i = 0; i < idx; i++) {
            newshape.push(this.shape[i])
        }
        this.shape = newshape
    }

    stepnodes(gap = 10, r = undefined) {
        // if (r > gap) throw 'r > gap'
        this.reseed(gap)
        if (r) r *= r
        let nodes = []
        let sumd = 0
        for (let i = 0; i < this.shape.length; i++) {
            let ip = (i + 1) % this.shape.length
            let pt0 = this.shape[i]
            let pt1 = this.shape[ip]
            let d = p5.Vector.dist(pt0, pt1)
            let pct = (gap - sumd) / d
            if (pct > 1) {
                sumd += d
                continue
            }
            let newn = p5.Vector.lerp(pt0, pt1, pct)
            if (r && nodes.reduce((acc, v) => {
                return acc || p5.Vector.sub(v, newn).magSq() < r
            }, false)) { continue }
            nodes.push(newn)
            sumd = (1 - pct) * d
        }
        return nodes
    }

    static line(x1, y1, x2, y2) {
        return new Poly([vec(x1, y1), vec(x2, y2)])
    }

    rotate(r, findBBox = 1, center = undefined) {
        this.tr += r
        center = center ?? this.centerOfMass()
        this.shape = this.shape.map(v =>
            v.copy().sub(center).rotate(r).add(center)
        )
        if (findBBox)
            this.findBBox()
        return this
    }

    translate(x, y, findBBox = 1) {
        this.tx += x
        this.ty += y
        this.shape = this.shape.map(v => {
            return vec(
                v.x + x,
                v.y + y
            )
        })
        if (findBBox)
            this.findBBox()
        return this
    }

    mult(s, findBBox = 1) {
        this.shape = this.shape.map(v => {
            return vec(
                v.x * s,
                v.y * s
            )
        })
        if (findBBox)
            this.findBBox()
        return this
    }

    bake() {
        this.rotate(this.r, 0)
        this.translate(this.x, this.y, 1)
        this.x = 0
        this.y = 0
        this.r = 0
        return this
    }

    subtract(other) {
        if (this.shape.length == 0) return other
        if (!this.path) {
            this.path = new paper.Path()
            this.shape.map((p, i) => {
                if (i == 0) this.path.moveTo(p.x, p.y)
                else this.path.lineTo(p.x, p.y)
                if (i == this.shape.length - 1 && this.closed) this.path.lineTo(this.shape[0].x, this.shape[0].y)
            })
        }
        // print(3, this, other)
        if (!other.path) {
            other.path = new paper.Path()
            other.shape.map((p, i) => {
                if (i == 0) other.path.moveTo(p.x, p.y)
                else other.path.lineTo(p.x, p.y)
                if (i == other.shape.length - 1 && other.closed) other.path.lineTo(other.shape[0].x, other.shape[0].y)
            })
        }
        // if one of the paths is compound then break it into smaller paths
        // let subbed = this.path.subtract(other.path, { trace: false })
        let subbed = this.path.subtract(other.path)
        // print(united)
        this.path = subbed
        // if (this.path.children) {
        //     print("more than one child")
        //     this.shape = []
        //     for (let child of this.path.children) {
        //         for (let seg of child.segments) {
        //             this.shape.push(vec(seg.point.x, seg.point.y))
        //         }
        //     }
        // } else {
        //     this.shape = united.segments.map(s => {
        //         return vec(s.point.x, s.point.y)
        //     }
        //     )
        // }
        this.findBBox()
        return this
    }


    // Morph two images according to a set of correspondence lines
    morph(initials, finals, alpha = 1, spineMode = false) {
        if (spineMode) {
            let newInitials = []
            let newFinals = []
            for (let i = 0; i < initials.length; i += 2) {
                newInitials.push([initials[i], initials[i + 1]])
                newFinals.push([finals[i], finals[i + 1]])
            }
            initials = newInitials
            finals = newFinals
        }

        const p = 0.5
        const a = 0.01
        const b = 2

        initials = initials.map(i => i.shape)
        finals = finals.map(f => f.shape)

        // helper function that returns poly given lines to interpolate to
        const warp = (shape, initials, finals) => {
            if (initials.length != finals.length) throw 'correspondences dont align'
            let newshape = []
            for (let i = 0; i < shape.length; i++) {
                // for (let j = 0; j < newImg.height; j++) {
                // keep track of totals for later normalization
                let dsum = new Vec(0, 0)
                let weightsum = 0
                let X = new Vec(shape[i].x, shape[i].y)
                for (let k = 0; k < initials.length; k++) {
                    // create necessary points
                    let P = new Vec(initials[k][0].x, initials[k][0].y)
                    let Q = new Vec(initials[k][1].x, initials[k][1].y)
                    let Pp = new Vec(finals[k][0].x, finals[k][0].y)
                    let Qp = new Vec(finals[k][1].x, finals[k][1].y)
                    // vector math from slides
                    // u is distance along line
                    const u = X.sub(P).dot(Q.sub(P)) / (Q.sub(P).len() ** 2)
                    // v is distance from line
                    const v = X.sub(P).dot(Q.sub(P).perp()) / Q.sub(P).len()
                    // Xp is calculated new point of X
                    const Xp = Pp.add(
                        Qp.sub(Pp).mult(u))
                        .add(
                            Qp.sub(Pp).perp().mult(v).div(Qp.sub(Pp).len()))
                    // Di is amount of displacement
                    const Di = Xp.sub(X)
                    // distance to line segment depends on distance along line
                    let d;
                    if (u < 0) d = X.sub(P).len()
                    else if (u < 1) d = Math.abs(v)
                    else d = X.sub(Q).len()
                    // weight using given fine-tuned parameters
                    const weight = ((Pp.sub(Qp).len() ** p) / (a + d)) ** b
                    dsum = dsum.add(Di.mult(weight))
                    weightsum += weight
                }
                // normalize
                const Xp = X.add(dsum.div(weightsum))
                newshape.push(vec(Xp.x, Xp.y))
                // newImg.setPixel(X.x, X.y, image.getPixel(Xp.x, Xp.y))
                // }
            }
            return newshape
        }

        // calculate intermediate line steps based on alpha
        let alphalines = []
        for (let i = 0; i < initials.length; i++) {

            let p1 = p5.Vector.lerp(initials[i][0], finals[i][0], alpha)
            let p2 = p5.Vector.lerp(initials[i][1], finals[i][1], alpha)
            alphalines.push([p1, p2])
        }
        // warp start and final images based on intermediate step
        let newShape = warp(this.shape, initials, alphalines)

        return new Poly(newShape)
    }

    unite(other) {
        // this.draw()
        // other.draw()
        // print(1, this, other)
        if (this.shape.length == 0) return other
        // print(2, this, other)

        if (!this.path) {
            this.path = new paper.Path()
            this.shape.map((p, i) => {
                if (i == 0) this.path.moveTo(p.x, p.y)
                else this.path.lineTo(p.x, p.y)
                if (i == this.shape.length - 1 && this.closed) this.path.lineTo(this.shape[0].x, this.shape[0].y)
            })
        }
        // print(3, this, other)
        if (!other.path) {
            other.path = new paper.Path()
            other.shape.map((p, i) => {
                if (i == 0) other.path.moveTo(p.x, p.y)
                else other.path.lineTo(p.x, p.y)
                if (i == other.shape.length - 1 && other.closed) other.path.lineTo(other.shape[0].x, other.shape[0].y)
            })
        }
        // print(4, this, other)
        // print(this.path, other.path)
        let united = this.path.unite(other.path)
        // print(united)
        this.path = united
        // if (this.path.children) {
        //     print("more than one child")
        //     this.shape = []
        //     for (let child of this.path.children) {
        //         for (let seg of child.segments) {
        //             this.shape.push(vec(seg.point.x, seg.point.y))
        //         }
        //     }
        // } else {
        //     this.shape = united.segments.map(s => {
        //         return vec(s.point.x, s.point.y)
        //     }
        //     )
        // }
        this.findBBox()
        return this
    }

    intersectionsPerPoly(polys, center) {
        let intersPerPoly = []
        for (let poly of polys) {
            let inters = this.intersections([poly])
            inters = inters.sort((a, b) => -distSq(a, center) + distSq(b, center))
            if (inters.length) {
                intersPerPoly.push(inters[0])
            }
        }
        // also add the point that is furthest away from the center
        // intersPerPoly.push(this.shape.reduce((acc, v) => {
        //     let d = distSq(v, center)
        //     if (d > acc.d) {
        //         acc.d = d
        //         acc.v = v
        //     }
        //     return acc
        // }, { d: 0, v: vec(0, 0) }).v)
        return intersPerPoly
    }

    intersections(polys) {
        let inters = []
        for (let poly of polys) {
            if (!this.BBoxOverlap(poly)) continue
            for (let i = 0; i < this.shape.length; i++) {
                let j = (i + 1) % this.shape.length;
                for (let k = 0; k < poly.shape.length; k++) {
                    let l = (k + 1) % poly.shape.length;
                    let pt = Poly.intersect(
                        this.shape[i],
                        this.shape[j],
                        poly.shape[k],
                        poly.shape[l])
                    if (pt)
                        inters.push(pt)

                }
            }
        }
        return inters
    }

    rndPointInPoly() {
        let pt
        do {
            pt = vec(rnd(this.bbl, this.bbr), rnd(this.bbt, this.bbb))
        } while (!this.contains(pt))
        return pt
    }


    static ellipse(x, y, r, r2 = undefined, arc = 3, rot = 0) {
        if (r <= 0.2) r = 0.2
        r2 = r2 ?? r
        let a = arc / max(r, r2)
        let shape = []
        let start = rnd(TAU)
        for (let i = start; i < TAU + start; i += a) {
            shape.push(vec(x + r * cos(i), y + r2 * sin(i)))
        }
        return new Poly(shape, 0, 0, 1, rot, 1)
    }

    static person(x = 0, y = 0, s = 1, r = 0, closed = true, c = undefined, sc = undefined) {
        let pp = [vec(99, 371), vec(132, 342), vec(155, 300), vec(206, 220), vec(232, 163), vec(270, 16), vec(230, 86), vec(215, 122), vec(203, 152), vec(170, 207), vec(144, 238), vec(128, 246), vec(147, 196), vec(176, 86), vec(184, 24), vec(192, -41), vec(207, -189), vec(212, -282), vec(215, -441), vec(210, -454), vec(174, -394), vec(167, -378), vec(143, -282), vec(124, -213), vec(94, -109), vec(91, -101), vec(75, 48), vec(56, -37), vec(24, -125), vec(-5, -234), vec(-37, -313), vec(-81, -390), vec(-125, -480), vec(-122, -450), vec(-113, -348), vec(-90, -205), vec(-69, -97), vec(-40, -16), vec(-4, 103), vec(34, 215), vec(47, 254), vec(31, 234), vec(4, 191), vec(-29, 130), vec(-70, 60), vec(-112, 6), vec(-90, 59), vec(-46, 170), vec(-9, 268), vec(14, 330), vec(40, 359), vec(47, 379), vec(42, 394), vec(35, 410), vec(38, 423), vec(48, 438), vec(70, 452), vec(87, 444), vec(107, 430), vec(108, 403), vec(96, 382),]
        pp.reverse()
        return new Poly(pp, x, y, s / 100, r + PI, closed, c, sc)
    }


    static rect(x, y, w, h) {
        w /= 2
        h /= 2
        let eps = 0.000001
        let shape = [
            vec(x - w, y - h),
            vec(x + w, y - h),
            vec(x + w + eps, y + h),
            vec(x - w - eps, y + h),
            vec(x - w, y - h)
        ]
        let poly = new Poly(shape)
        return poly
    }


    static order(polys, start = 0, pct = 1) {
        let ordered = []
        let coms = polys.map((p, i) => { return [p.centerOfMass(), i] })
        let curr = coms.splice(start, 1)[0]
        while (ordered.length < polys.length * pct) {
            coms = coms.sort((a, b) => {
                let d1 = p5.Vector.sub(curr[0], a[0]).magSq()
                let d2 = p5.Vector.sub(curr[0], b[0]).magSq()
                return d1 - d2
            })
            curr = coms.shift()
            ordered.push(polys[curr[1]])
        }
        return ordered
    }


    restructure(tol = 0.12, alsoReseed = 5) {
        let shape = [this.shape[0]]
        for (let i = 0; i < this.shape.length - 1; i++) {
            let ip = (i + 1) % this.shape.length
            let ipp = (i + 2) % this.shape.length
            let p0 = shape[shape.length - 1]
            let p1 = this.shape[ip]
            let p2 = this.shape[ipp]
            let v0 = p5.Vector.sub(p1, p0)
            let v1 = p5.Vector.sub(p2, p1)
            if (abs(v0.angleBetween(v1)) > tol)
                shape.push(p1)
        }
        this.shape = shape
        if (alsoReseed)
            this.reseed(alsoReseed)
        return this
    }


    reflect(angles, c = undefined, reflectionOnly = false, keepAll = false) {
        c = c ?? this.centerOfMass()
        let shape = this.shape
        for (let j = 0; j < angles.length; j++) {
            let angle = angles[j]
            let newshape = []
            let refline = vec(1, 0).rotate(angle)
            refline.setMag(39000)
            let start
            if (keepAll) newshape = shape
            else
                for (let i = 0; i < shape.length; i++) {
                    let v = shape[i]
                    let dir = p5.Vector.sub(v, c)
                    if (dir.cross(refline).z > 0) {
                        newshape.push(v)
                    }
                    else
                        start = start ?? i
                }
            refline.rotate(PI / 2)
            newshape = newshape.concat(newshape.splice(0, start))
            let len = newshape.length
            for (let i = len - 1; i >= 0; i--) {
                let v = vec(newshape[i].x, newshape[i].y)
                v.sub(c)
                let newv = v.reflect(refline)
                newv.add(c)
                newshape.push(newv)
            }
            shape = newshape
            if (reflectionOnly) shape.splice(0, len)
        }
        this.shape = shape
        this.findBBox()
        return this
    }

    static reflectAll(polys, angles, centers, reflectionOnly = true, keepAll = true) {
        for (let i = 0; i < angles.length; i++) {
            let a = angles[i]
            let c = centers[i % centers.length]
            let cp = polys.map(p => p.copy())
            cp = cp.map(p => p.reflect([a], c, reflectionOnly, keepAll))
            polys = polys.map((p, i) => [p, cp[i]]).flat()
        }
        return polys
    }

    copy(x = undefined, y = undefined, s = 1, c = undefined, sc = undefined) {
        x = x ?? 0
        y = y ?? 0
        s = s ?? 1
        c = c ?? this.c
        sc = sc ?? this.sc
        return new Poly(this.shape, x, y, s, 0, this.closed, c, sc)
    }

    setValue(v) {
        this.value = v
        return this
    }

    setColor(c = undefined, sc = undefined) {
        this.c = c
        this.sc = sc
        return this
    }


    onCanvas(lm = 0, rm = W, tm = 0, bm = H) {
        return (this.bbl > lm &&
            this.bbr < rm &&
            this.bbt > tm &&
            this.bbb < bm)
    }

    static intersect = (l0p0, l0p1, l1p0, l1p1) => {
        let x1 = l0p0.x
        let y1 = l0p0.y
        let x2 = l0p1.x
        let y2 = l0p1.y
        let x3 = l1p0.x
        let y3 = l1p0.y
        let x4 = l1p1.x
        let y4 = l1p1.y
        var a_dx = x2 - x1;
        var a_dy = y2 - y1;
        var b_dx = x4 - x3;
        var b_dy = y4 - y3;
        var s = (-a_dy * (x1 - x3) + a_dx * (y1 - y3)) / (-b_dx * a_dy + a_dx * b_dy);
        var t = (+b_dx * (y1 - y3) - b_dy * (x1 - x3)) / (-b_dx * a_dy + a_dx * b_dy);
        return (s >= 0 && s <= 1 && t >= 0 && t <= 1) ? [x1 + t * a_dx, y1 + t * a_dy] : false;
    }

    findBBox() {
        this.bbl = 999999;
        this.bbr = -999999;
        this.bbt = 999999;
        this.bbb = -999999;

        for (let p of this.shape) {
            if (p.x < this.bbl) this.bbl = p.x;
            if (p.x > this.bbr) this.bbr = p.x;
            if (p.y < this.bbt) this.bbt = p.y;
            if (p.y > this.bbb) this.bbb = p.y;
        }
    }

    BBoxOverlap(poly) {
        return (this.bbr > poly.bbl && this.bbb > poly.bbt) &&
            (this.bbr > poly.bbl && this.bbt < poly.bbb) &&
            (this.bbl < poly.bbr && this.bbb > poly.bbt) &&
            (this.bbl < poly.bbr && this.bbt < poly.bbb)
    }


    //https://stackoverflow.com/questions/16285134/calculating-polygon-area
    getArea() {
        let vertices = this.shape
        var total = 0;
        for (var i = 0, l = vertices.length; i < l; i++) {
            var addX = vertices[i].x;
            var addY = vertices[i == vertices.length - 1 ? 0 : i + 1].y;
            var subX = vertices[i == vertices.length - 1 ? 0 : i + 1].x;
            var subY = vertices[i].y;

            total += (addX * addY * 0.5);
            total -= (subX * subY * 0.5);
        }

        return Math.abs(total);
    }

    // for closed shapes
    getPerimeterSq() {
        return this.shape.reduce((perim, v, i) => {
            let j = (i + 1) % this.shape.length
            return perim + p5.Vector.magSq(p5.Vector.sub(v, this.shape[j]))
        }, 0)
    }

    contains(p) {
        // Check if the dot is roughly in the region 
        if (p.x < this.bbl || p.x > this.bbr
            || p.y < this.bbt || p.y > this.bbb) {
            return false;
        }

        // Create dot2 as the other end of the imaginary horizontal line extending off edge of canvas
        let off = vec(999999, p.y);
        // Check each line around this polygon, and count up the number of intersects
        let intersections = 0;
        this.shape.map((_, i) => {
            let j = (i + 1) % this.shape.length;
            intersections += Poly.intersect(p, off, this.shape[i], this.shape[j]);
        })

        // If it's even, the dot is outside
        // stroke(intersections % 2 * 255, 0, 0)
        // circle(p.x, p.y, 20)
        return !(intersections % 2 == 0)
    }

    overlaps(poly, andNotInside = false) {
        if (!this.BBoxOverlap(poly)) return false

        for (let i = 0; i < this.shape.length; i++) {
            let j = (i + 1) % this.shape.length;
            for (let k = 0; k < poly.shape.length; k++) {
                let l = (k + 1) % poly.shape.length;
                if (Poly.intersect(
                    this.shape[i],
                    this.shape[j],
                    poly.shape[k],
                    poly.shape[l]))
                    return true
            }
        }
        if (andNotInside) {
            return poly.contains(this.shape[0]) || this.contains(poly.shape[0])
        }
        return false
    }

    // checks if poly overlaps with canvas or an array of polys
    overlapsAny(polys, andNotOnCanvas = true, andNotInside = true) {
        return (andNotOnCanvas && !this.onCanvas()) || polys.reduce((canPack, poly2) => {
            return canPack || this.overlaps(poly2, andNotInside)
        }, false)
    }


    distort(s = 100, m = 500, off = 0, rand = false) {
        this.shape = this.shape.map(v => {
            return vec(
                v.x + (rand ? rnd(-s, s) : s * sn(v.x / m, v.y / m, 100 + off)),
                v.y + (rand ? rnd(-s, s) : s * sn(v.x / m, v.y / m, 1000 + off))
            )
        })

        this.findBBox()
        return this
    }

    sindistort(a, b, off) {
        this.shape = this.shape.map(v => {
            let normPos = (v.x - this.bbl) / (this.bbr - this.bbl) * TAU;
            return vec(
                v.x,
                v.y - a * sin(b * normPos + off)
            )
        })

        this.findBBox()
    }

    wrinkle(n = 100, amt = 16, reseeded = false, mini = 100, maxi = 800, centered = true, off = 0,) {
        let com;
        if (centered) com = this.centerOfMass()
        for (let i = 0; i < n; i++) {
            this.distort(amt, rnd(mini, maxi), off, false, false)
            if (reseeded)
                this.reseed(reseeded)
        }
        if (centered) {
            let newcom = this.centerOfMass()
            let trans = p5.Vector.sub(newcom, com)
            this.shape = this.shape.map(v => vec(v.x - trans.x, v.y - trans.y))
            this.findBBox()
            return this
        }
        this.findBBox()
        return this
    }

    reseed(gap = 5) {
        if (gap == 0) return this
        let shape = []
        for (let i = 0; i < this.shape.length; i++) {
            let ip = (i + 1) % this.shape.length
            let v1 = this.shape[i]
            let v2 = this.shape[ip]
            let d = p5.Vector.dist(v1, v2)
            let percent = gap / d
            shape.push(v1)
            if (percent < 1) {
                if (percent > 0.5) {
                    shape.push(p5.Vector.lerp(v1, v2, 0.5))
                } else
                    for (let j = percent; j < 1; j += percent) {
                        shape.push(p5.Vector.lerp(v1, v2, j))
                    }
            }
        }
        this.shape = shape
        return this
    }


    centerOfMass() {
        return p5.Vector.div(this.shape.reduce((prev, curr) => {
            prev.add(curr)
            return prev
        }, vec(0, 0)), this.shape.length)
    }


    resize(x, y, w, h, r = 0) {
        w = w ?? this.bbr - this.bbl
        h = h ?? this.bbb - this.bbt

        let com = vec((this.bbl + this.bbr) / 2, (this.bbb + this.bbt) / 2)
        this.shape = this.shape.map((v) => {
            v.sub(com)
            v.mult(vec(w / (this.bbr - this.bbl), h / (this.bbb - this.bbt)))
            let rv = p5.Vector.rotate(v, r)
            return vec(
                x + rv.x,
                y + rv.y
            )
        })
        this.findBBox()
        return this
    }

    draw() {
        push()
        if (this.c != undefined) {
            if (this.c == -1) noFill()
            else
                fill(this.c)
        }
        if (this.sc != undefined) {
            if (this.sc == -1) noStroke()
            else
                stroke(this.sc)
        }

        beginShape()
        this.shape.map((v, i) => {
            vertex(v.x, v.y)
        })
        endShape(CLOSE)
        // this.drawNodes()

        pop()
        return this
    }


    drawNodes(r = 3) {
        for (let p of this.shape) {
            // circle(p.x, p.y, r)
            let c = new paper.Path.Circle(new paper.Point(p.x, p.y), r);
            c.fillColor = 'black'

        }
    }

    drawBBox(color) {
        push()
        strokeWeight(1)
        stroke(color)
        rect(this.bbl, this.bbt, this.bbr - this.bbl, this.bbb - this.bbt)
        pop()
    }
}
// vector math helper class
class Vec {
    constructor(x, y) {
        this.x = x
        this.y = y
    }
    add(v) { return new Vec(this.x + v.x, this.y + v.y) }

    sub(v) { return new Vec(this.x - v.x, this.y - v.y) }

    mult(s) { return new Vec(this.x * s, this.y * s) }

    div(s) { return new Vec(this.x / s, this.y / s) }

    dot(v) { return (this.x * v.x) + (this.y * v.y) }

    len() { return dist(0, 0, this.x, this.y) }
    //normalize
    norm() { return this.div(this.len()) }
    //find an orthogonal vector
    perp() { return new Vec(this.y, -this.x) }

}